import os
import ssl
from typing import Any, Callable

import elastic_transport
import elasticsearch as es
from chesse.v1alpha1 import games_pb2, positions_pb2
from loguru import logger

from backend.search_engine.controller import interface as controller_if
from backend.search_engine.query import elasticsearch as es_query
from backend.tracing import tracer
from backend.utils import exception


def _parse_es_instance_env_vars() -> tuple[str, str, str, str]:
    url = os.getenv("ELASTICSEARCH_HOSTS")

    username = os.getenv("ELASTICSEARCH_USERNAME")
    password = os.getenv("ELASTICSEARCH_PASSWORD")
    if not username or not password:
        raise exception.InvalidCredentialsError("Username or password not provided.")

    cert_path = os.getenv("ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES")
    if not os.path.isfile(cert_path):
        raise exception.InvalidCredentialsError(
            f"Certificate file at location {cert_path} does not exist."
        )

    return (url, username, password, cert_path)


def _es_bucket_to_chess_position_rating_stats_pb(
    bucket: dict[str, Any],
) -> positions_pb2.ChessPositionRatingStats:
    position_rtg_stats_pb = positions_pb2.ChessPositionRatingStats(
        min=int(min(bucket["white"]["min_elo"]["value"], bucket["black"]["min_elo"]["value"])),
        avg=int((bucket["white"]["avg_elo"]["value"] + bucket["black"]["avg_elo"]["value"]) / 2),
        max=int(max(bucket["white"]["max_elo"]["value"], bucket["black"]["max_elo"]["value"])),
    )

    return position_rtg_stats_pb


def _es_bucket_to_chess_position_result_stats_pb(
    bucket: dict[str, Any],
) -> positions_pb2.ChessPositionStats:
    position_res_stats_pb = positions_pb2.ChessPositionResultStats(
        white_win_pct=0, draw_pct=0, black_win_pct=0
    )

    for side in bucket["results"]["side_won"]["buckets"]:
        win_rate_pct = side["doc_count"] / bucket["doc_count"] * 100
        match side["key"]:
            case 1:
                position_res_stats_pb.white_win_pct = win_rate_pct
            case 0.5:
                position_res_stats_pb.draw_pct = win_rate_pct
            case 0:
                position_res_stats_pb.black_win_pct = win_rate_pct
            case _:
                raise exception.SearchEnginePbConversionError(
                    f"Illegal winning side: {side['key']}"
                )

    return position_res_stats_pb


def _es_bucket_to_chess_position_pb(
    bucket: dict[str, Any], fen_encoding
) -> positions_pb2.ChessPositionStats:
    nr_games = bucket["doc_count"]
    position_rtg_stats_pb = _es_bucket_to_chess_position_rating_stats_pb(bucket)
    position_res_stats_pb = _es_bucket_to_chess_position_result_stats_pb(bucket)

    position_pb = positions_pb2.ChessPosition(
        fen_encoding=fen_encoding,
        position_stats=positions_pb2.ChessPositionStats(
            nr_games=nr_games,
            rating_stats=position_rtg_stats_pb,
            result_stats=position_res_stats_pb,
        ),
    )

    return position_pb


def _es_hit_to_chess_game_pb(hit) -> games_pb2.ChessGame:
    chess_game_ctx_pb = games_pb2.ChessGameContext(
        event=hit["_source"]["context"]["event"],
        date=hit["_source"]["context"]["date"],
        site=hit["_source"]["context"]["site"],
        round=hit["_source"]["context"]["round"],
    )
    white_pb = games_pb2.White(
        name=hit["_source"]["white"]["name"], elo=hit["_source"]["white"]["elo"]
    )
    black_pb = games_pb2.Black(
        name=hit["_source"]["black"]["name"], elo=hit["_source"]["black"]["elo"]
    )
    moves_pb = [
        games_pb2.Move(uci=move["uci"], san=move["san"], fen=move["fen"])
        for move in hit["_source"]["moves"]
    ]

    chess_game_pb = games_pb2.ChessGame(
        id=hit["_source"]["id"],
        context=chess_game_ctx_pb,
        white=white_pb,
        black=black_pb,
        moves=moves_pb,
        result=hit["_source"]["result"],
    )

    return chess_game_pb


def _es_response_to_chess_position_pb(
    response: dict[str, Any], fen_encoding: str
) -> positions_pb2.ChessPositionStats:
    bucket = response["aggregations"]["by_fen"]["fen"]["buckets"][0]
    position_pb = _es_bucket_to_chess_position_pb(bucket, fen_encoding=fen_encoding)

    return position_pb


def _es_response_to_chess_positions_pb(
    response: dict[str, Any]
) -> list[positions_pb2.ChessPosition]:
    chess_positions_pb = []
    for bucket in response["aggregations"]["by_fen"]["fen"]["buckets"]:
        chess_position_pb = _es_bucket_to_chess_position_pb(
            bucket, fen_encoding=bucket["key"].partition(" ")[0]
        )
        chess_positions_pb.append(chess_position_pb)

    return chess_positions_pb


def _es_response_to_chess_game_pb(response: dict[str, Any]) -> games_pb2.ChessGame:
    chess_game_pb = _es_hit_to_chess_game_pb(response["hits"]["hits"][0])

    return chess_game_pb


def _es_response_to_chess_games_pb(response: dict[str, Any]) -> list[games_pb2.ChessGame]:
    chess_games_pb = []
    for hit in response["hits"]["hits"]:
        chess_game_pb = _es_hit_to_chess_game_pb(hit)
        chess_games_pb.append(chess_game_pb)

    return chess_games_pb


def _exception_handler(func: Callable):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (elastic_transport.ApiError, elastic_transport.TransportError) as e:
            raise exception.SearchEngineError(f"Elasticsearch call failed: {e}")
        except AttributeError as e:
            raise exception.SearchEnginePbConversionError(f"Cannot convert to pb object: {e}.")

    return handler


class ElasticsearchController(controller_if.AbstractSearchEngineController):
    @_exception_handler
    def __init__(self) -> None:
        (url, username, password, cert_path) = _parse_es_instance_env_vars()

        ssl_context = ssl.create_default_context(cafile=cert_path)
        self.client = es.Elasticsearch(url, http_auth=(username, password), ssl_context=ssl_context)

        logger.info(f"Initialised Search Engine Controller at {url}.")

    @_exception_handler
    def get_chess_position_pb(self, fen_encoding: str) -> positions_pb2.ChessPosition:
        query = es_query.get_chess_position_query(fen_encoding)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response = self.client.search(index="games", body=query)

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get position by FEN encoding {fen_encoding!r}."
            )

        chess_position_pb = _es_response_to_chess_position_pb(response, fen_encoding=fen_encoding)

        return chess_position_pb

    def _get_chess_positions_by_similarity_encoding(
        self, similarity_encoding: str
    ) -> list[positions_pb2.ChessPosition]:
        query_sim_pos = es_query.get_similar_positions_query(similarity_encoding)
        with tracer.start_as_current_span("Elasticsearch/positions/_search"):
            response_sim_pos = self.client.search(index="positions", body=query_sim_pos)

        if response_sim_pos["_shards"]["total"] != response_sim_pos["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get positions by similarity encoding {similarity_encoding!r}."
            )

        # FEN encodings of the similar positions
        fen_encodings = [
            chess_position["_source"]["position"]["fen_encoding"]
            for chess_position in response_sim_pos["hits"]["hits"]
        ]

        query_position_stats = es_query.get_chess_positions_stats_query(fen_encodings)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response_positions_stats = self.client.search(index="games", body=query_position_stats)

        if (
            response_positions_stats["_shards"]["total"]
            != response_positions_stats["_shards"]["successful"]
        ):
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get positions stats by FEN encodings {fen_encodings!r}."
            )

        chess_positions_pb = _es_response_to_chess_positions_pb(response_positions_stats)

        return chess_positions_pb

    @_exception_handler
    def get_chess_positions_pb(self, **kwargs: Any) -> list[positions_pb2.ChessPosition]:
        match list(kwargs.keys()):
            case ["similarity_encoding"]:
                return self._get_chess_positions_by_similarity_encoding(
                    similarity_encoding=kwargs["similarity_encoding"]
                )
            case _:
                raise exception.IllegalArgumentError(
                    f"Invalid arguments to function get_chess_positions: {kwargs}."
                )

    @_exception_handler
    def get_chess_game_pb(self, id: str) -> games_pb2.ChessGame:
        query = es_query.get_game_query(id)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response = self.client.search(index="games", body=query)

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(f"Query unsuccessful: get game by id {id!r}.")
        if not response["hits"]["hits"]:
            raise exception.NotFoundError(f"Game not found: {id!r}.")

        chess_game_pb = _es_response_to_chess_game_pb(response)

        return chess_game_pb

    def _get_chess_games_by_fen_encoding(self, fen_encoding: str) -> list[games_pb2.ChessGame]:
        query = es_query.get_games_query(fen_encoding)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response = self.client.search(index="games", body=query)

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get games by FEN encoding {fen_encoding!r}."
            )

        chess_games_pb = _es_response_to_chess_games_pb(response)

        return chess_games_pb

    @_exception_handler
    def get_chess_games_pb(self, **kwargs: Any) -> list[games_pb2.ChessGame]:
        match list(kwargs.keys()):
            case ["fen_encoding"]:
                return self._get_chess_games_by_fen_encoding(fen_encoding=kwargs["fen_encoding"])
            case _:
                raise exception.IllegalArgumentError(
                    f"Invalid arguments to function get_chess_positions: {kwargs}."
                )

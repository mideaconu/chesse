import os
import ssl
from typing import Any, Callable

import elastic_transport
import elasticsearch as es
import structlog
from chesse.v1alpha1 import games_pb2, positions_pb2

from backend.search_engine.controller import interface as controller_if
from backend.search_engine.query import elasticsearch as es_query
from backend.tracing import trace, tracer
from backend.utils import exception

logger = structlog.get_logger()


def _parse_es_instance_env_vars() -> tuple[str, str, str, str]:
    scheme = os.getenv("ELASTICSEARCH_SCHEME", "http")
    host = os.getenv("ELASTICSEARCH_HOST", "localhost")
    port = os.getenv("ELASTICSEARCH_PORT", "9200")
    url = f"{scheme}://{host}:{port}"
    structlog.contextvars.bind_contextvars(
        search_engine_scheme=scheme, search_engine_host=host, search_engine_port=port
    )

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
        min=int(min(bucket["white_elo"]["min"], bucket["black_elo"]["min"])),
        avg=int((bucket["white_elo"]["avg"] + bucket["black_elo"]["avg"]) / 2),
        max=int(max(bucket["white_elo"]["max"], bucket["black_elo"]["max"])),
    )

    return position_rtg_stats_pb


def _es_bucket_to_chess_position_result_stats_pb(
    bucket: dict[str, Any],
) -> positions_pb2.ChessPositionStats:
    position_res_stats_pb = positions_pb2.ChessPositionResultStats(
        white_win_pct=0, draw_pct=0, black_win_pct=0
    )

    for side in bucket["results"]["buckets"]:
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


def _es_bucket_to_chess_position_pb(bucket: dict[str, Any]) -> positions_pb2.ChessPositionStats:
    position_rtg_stats_pb = _es_bucket_to_chess_position_rating_stats_pb(bucket)
    position_res_stats_pb = _es_bucket_to_chess_position_result_stats_pb(bucket)

    position_pb = positions_pb2.ChessPosition(
        fen_encoding=bucket["key"],
        position_stats=positions_pb2.ChessPositionStats(
            nr_games=bucket["doc_count"],
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


def _es_response_to_chess_position_pb(response: dict[str, Any]) -> positions_pb2.ChessPositionStats:
    bucket = response["aggregations"]["positions"]["buckets"][0]
    position_pb = _es_bucket_to_chess_position_pb(bucket)

    return position_pb


def _es_response_to_chess_positions_pb(
    response: dict[str, Any], fen_encodings: list[str]
) -> list[positions_pb2.ChessPosition]:
    chess_positions_pb = [None] * len(fen_encodings)
    for bucket in response["aggregations"]["positions"]["buckets"]:
        chess_position_pb = _es_bucket_to_chess_position_pb(bucket)
        chess_positions_pb[fen_encodings.index(chess_position_pb.fen_encoding)] = chess_position_pb

    if None in chess_positions_pb:
        chess_positions_pb = [elem for elem in chess_positions_pb if elem is not None]
        logger.warning(
            "elasticsearch returned less positions than the number of similar positions found",
            {
                "nr_similar_positions": len(fen_encodings),
                "nr_chess_positions": len(chess_positions_pb),
            },
        )

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
        except (KeyError, AttributeError) as e:
            raise exception.SearchEnginePbConversionError(f"Cannot convert to pb object: {e}.")

    return handler


class ElasticsearchController(controller_if.AbstractSearchEngineController):
    @_exception_handler
    def __init__(self) -> None:
        (url, username, password, cert_path) = _parse_es_instance_env_vars()

        ssl_context = ssl.create_default_context(cafile=cert_path)
        self.client = es.Elasticsearch(url, http_auth=(username, password), ssl_context=ssl_context)

        self.scroll_timeout = os.getenv("ELASTICSEARCH_SCROLL_TIMEOUT", "1m")

        logger.info("initialised search engine controller")

    @_exception_handler
    def get_chess_position_pb(self, fen_encoding: str) -> positions_pb2.ChessPosition:
        (query, runtime_mappings, aggs) = es_query.get_chess_position_query(fen_encoding)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response = self.client.search(
                index="games", query=query, runtime_mappings=runtime_mappings, aggs=aggs
            )

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get position by FEN encoding {fen_encoding!r}."
            )

        with tracer.start_as_current_span("output: pb conversion"):
            chess_position_pb = _es_response_to_chess_position_pb(response)

        return chess_position_pb

    def _get_similar_chess_position_fen_encodings(
        self, similarity_encoding: str, *, page_size: int, page_token: str
    ) -> tuple[list[str], str]:
        query = es_query.get_similar_positions_query(similarity_encoding)
        if not page_token:
            with tracer.start_as_current_span("Elasticsearch/positions/_search"):
                response = self.client.search(
                    index="positions", query=query, size=page_size, scroll=self.scroll_timeout
                )
        else:
            with tracer.start_as_current_span("Elasticsearch/_search/scroll"):
                response = self.client.scroll(scroll_id=page_token, scroll=self.scroll_timeout)

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get positions by similarity encoding {similarity_encoding!r}."
            )

        # FEN encodings of the similar positions
        fen_encodings = [
            chess_position["_source"]["position"]["fen_encoding"]
            for chess_position in response["hits"]["hits"]
        ]
        next_page_token = response["_scroll_id"]

        trace.get_current_span().add_event(
            "similar positions found",
            {
                "similar_positions": [
                    f"{(chess_position['_source']['position']['fen_encoding'], chess_position['_score'])}"
                    for chess_position in response["hits"]["hits"]
                ],
                "total_size": len(fen_encodings),
                "next_page_token": next_page_token,
            },
        )

        return (fen_encodings, next_page_token)

    @_exception_handler
    def get_chess_positions_pb(
        self, similarity_encoding: str, page_size: int, page_token: str
    ) -> tuple[list[positions_pb2.ChessPosition], int, str]:
        (fen_encodings, next_page_token,) = self._get_similar_chess_position_fen_encodings(
            similarity_encoding, page_size=page_size, page_token=page_token
        )
        (query, runtime_mappings, aggs) = es_query.get_chess_positions_query(fen_encodings)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response = self.client.search(
                index="games", query=query, runtime_mappings=runtime_mappings, aggs=aggs
            )

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get positions stats by FEN encodings {fen_encodings!r}."
            )

        with tracer.start_as_current_span("output: pb conversion"):
            chess_positions_pb = _es_response_to_chess_positions_pb(response, fen_encodings)
        total_size = len(chess_positions_pb)

        return chess_positions_pb, total_size, next_page_token

    @_exception_handler
    def get_chess_game_pb(self, id: str) -> games_pb2.ChessGame:
        query = es_query.get_chess_game_query(id)
        with tracer.start_as_current_span("Elasticsearch/games/_search"):
            response = self.client.search(index="games", query=query)

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(f"Query unsuccessful: get game by id {id!r}.")
        if not response["hits"]["hits"]:
            raise exception.NotFoundError(f"Game not found: {id!r}.")

        with tracer.start_as_current_span("output: pb conversion"):
            chess_game_pb = _es_response_to_chess_game_pb(response)

        return chess_game_pb

    @_exception_handler
    def get_chess_games_pb(
        self, fen_encoding: str, page_size: int, page_token: str
    ) -> tuple[list[games_pb2.ChessGame], int, str]:
        query = es_query.get_chess_games_query(fen_encoding)
        if not page_token:
            with tracer.start_as_current_span("Elasticsearch/games/_search"):
                response = self.client.search(
                    index="games", query=query, size=page_size, scroll=self.scroll_timeout
                )
        else:
            with tracer.start_as_current_span("Elasticsearch/_search/scroll"):
                response = self.client.scroll(scroll_id=page_token, scroll=self.scroll_timeout)

        if response["_shards"]["total"] != response["_shards"]["successful"]:
            raise exception.SearchEngineQueryError(
                f"Query unsuccessful: get games by FEN encoding {fen_encoding!r}."
            )

        with tracer.start_as_current_span("output: pb conversion"):
            chess_games_pb = _es_response_to_chess_games_pb(response)
        total_size = len(chess_games_pb)
        next_page_token = response["_scroll_id"]

        return chess_games_pb, total_size, next_page_token

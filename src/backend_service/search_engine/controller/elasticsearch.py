import os
import ssl
from typing import Any, List

import elasticsearch as es
import elasticsearch_dsl as es_dsl
from chesse.v1alpha1 import games_pb2, positions_pb2
from elasticsearch_dsl.response import Response
from elasticsearch_dsl.response.aggs import FieldBucket
from loguru import logger

from backend_service.search_engine.controller import interface as controller_if
from backend_service.utils import exception


def _log_and_raise_pb_conversion_error(response: Response, pb_object: Any, error: str) -> None:
    err_msg = f"Cannot convert response {response.to_dict()} to pb object {pb_object}: {error}."
    logger.error(err_msg)
    raise exception.SearchEnginePbConversionError(err_msg)


def _es_bucket_to_chess_position_rating_stats_pb(
    bucket: FieldBucket,
) -> positions_pb2.ChessPositionRatingStats:
    position_rtg_stats_pb = positions_pb2.ChessPositionRatingStats(
        min=int(min(bucket.white.min_elo.value, bucket.black.min_elo.value)),
        avg=int((bucket.white.avg_elo.value + bucket.black.avg_elo.value) / 2),
        max=int(max(bucket.white.max_elo.value, bucket.black.max_elo.value)),
    )

    return position_rtg_stats_pb


def _es_bucket_to_chess_position_result_stats_pb(
    bucket: FieldBucket,
) -> positions_pb2.ChessPositionStats:
    position_res_stats_pb = positions_pb2.ChessPositionResultStats(
        white_win_pct=0, draw_pct=0, black_win_pct=0
    )

    for side in bucket.results.side_won.buckets:
        win_rate_pct = side.doc_count / bucket.doc_count * 100
        match side.key:
            case 1:
                position_res_stats_pb.white_win_pct = win_rate_pct
            case 0.5:
                position_res_stats_pb.draw_pct = win_rate_pct
            case 0:
                position_res_stats_pb.black_win_pct = win_rate_pct
            case _:
                err_msg = f"Illegal winning side: {side['key']}"
                logger.error(err_msg)
                raise exception.SearchEnginePbConversionError(err_msg)

    return position_res_stats_pb


def _es_bucket_to_chess_position_pb(
    bucket: FieldBucket, fen_encoding
) -> positions_pb2.ChessPositionStats:
    nr_games = bucket.doc_count
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
        event=hit.context.event,
        date=hit.context.date,
        site=hit.context.site,
        round=hit.context.round,
    )
    white_pb = games_pb2.White(name=hit.white.name, elo=hit.white.elo)
    black_pb = games_pb2.Black(name=hit.black.name, elo=hit.black.elo)
    moves_pb = [games_pb2.Move(uci=move.uci, san=move.san, fen=move.fen) for move in hit.moves]

    chess_game_pb = games_pb2.ChessGame(
        id=hit.id,
        context=chess_game_ctx_pb,
        white=white_pb,
        black=black_pb,
        moves=moves_pb,
        result=hit.result,
    )

    return chess_game_pb


def _es_response_to_chess_position_pb(
    response: Response, fen_encoding: str
) -> positions_pb2.ChessPositionStats:
    try:
        bucket = response.aggregations.category_fen.fen.buckets[0]
        position_pb = _es_bucket_to_chess_position_pb(bucket, fen_encoding=fen_encoding)
    except AttributeError as e:
        _log_and_raise_pb_conversion_error(
            response=response, pb_object=List[games_pb2.ChessGame], error=e
        )

    return position_pb


def _es_response_to_chess_positions_pb(response: Response) -> List[positions_pb2.ChessPosition]:
    chess_positions_pb = []
    try:
        for bucket in response.aggregations.category_fen.fen.buckets:
            chess_position_pb = _es_bucket_to_chess_position_pb(
                bucket, fen_encoding=bucket.key.partition(" ")[0]
            )
            chess_positions_pb.append(chess_position_pb)
    except AttributeError as e:
        _log_and_raise_pb_conversion_error(
            response=response, pb_object=List[games_pb2.ChessGame], error=e
        )

    return chess_positions_pb


def _es_response_to_chess_game_pb(response: Response) -> games_pb2.ChessGame:
    try:
        chess_game_pb = _es_hit_to_chess_game_pb(response.hits[0])
    except AttributeError as e:
        _log_and_raise_pb_conversion_error(
            response=response, pb_object=List[games_pb2.ChessGame], error=e
        )

    return chess_game_pb


def _es_response_to_chess_games_pb(response: Response) -> List[games_pb2.ChessGame]:
    chess_games_pb = []
    try:
        for hit in response.hits:
            chess_game_pb = _es_hit_to_chess_game_pb(hit)
            chess_games_pb.append(chess_game_pb)
    except AttributeError as e:
        _log_and_raise_pb_conversion_error(
            response=response, pb_object=List[games_pb2.ChessGame], error=e
        )

    return chess_games_pb


def _check_query_is_successful(query: es_dsl.Search, response: Response) -> None:
    if not response.success():
        error_message = f"Query unsuccessful: {query.to_dict()}."
        logger.error(error_message)
        raise exception.SearchEngineQueryError(error_message)


class ElasticsearchController(controller_if.AbstractSearchEngineController):
    def __init__(self) -> None:
        url = os.getenv("SEARCH_ENGINE_URL", "https://localhost:9200")
        username = os.getenv("SEARCH_ENGINE_USERNAME")
        password = os.getenv("SEARCH_ENGINE_PASSWORD")

        if not username or not password:
            raise exception.InvalidCredentialsError("Username or password not provided.")

        context = ssl.create_default_context(cafile="/Users/mihaideaconu/Documents/http_ca.crt")
        self.client = es.Elasticsearch(url, http_auth=(username, password), ssl_context=context)

        logger.info(f"Initialised Search Engine Controller at {url}.")

    def get_chess_position_pb(self, fen_encoding: str) -> positions_pb2.ChessPosition:
        # There is a difference between the FEN encoding of a move and a position. The fen encoding
        # of a move contains additional information about the state of the game after the move is
        # made (e.g. side to move, castling, en-passant rights):
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # Because of that, we ignore everything that follows the position FEN encoding in the query
        fen_encoding_regex = f"{fen_encoding}.*"

        query = es_dsl.Search(using=self.client, index="games").query(
            "nested", path="moves", query=es_dsl.Q("regexp", moves__fen=fen_encoding_regex)
        )
        query.aggs.bucket("category_fen", "nested", path="moves").bucket(
            "fen", "terms", field="moves.fen", include=fen_encoding_regex
        )
        query.aggs["category_fen"]["fen"].bucket("white", "reverse_nested").metric(
            "min_elo", "min", field="white.elo"
        ).metric("max_elo", "max", field="white.elo").metric("avg_elo", "avg", field="white.elo")
        query.aggs["category_fen"]["fen"].bucket("black", "reverse_nested").metric(
            "min_elo", "min", field="black.elo"
        ).metric("max_elo", "max", field="black.elo").metric("avg_elo", "avg", field="black.elo")
        query.aggs["category_fen"]["fen"].bucket("results", "reverse_nested").metric(
            "side_won", "terms", field="result"
        )

        response = query.execute()
        _check_query_is_successful(query=query, response=response)

        chess_position_pb = _es_response_to_chess_position_pb(response, fen_encoding=fen_encoding)

        return chess_position_pb

    def _get_chess_positions_by_similarity_encoding(
        self, similarity_encoding: str
    ) -> List[positions_pb2.ChessPosition]:
        # Querying similar positions using the similarity encoding
        query_similar_positions = es_dsl.Search(using=self.client, index="positions").query(
            "match", position__similarity_encoding=similarity_encoding
        )

        response_similar_positions = query_similar_positions.execute()
        _check_query_is_successful(
            query=query_similar_positions, response=response_similar_positions
        )

        similar_positions_fen_encodings = [
            chess_position.position.fen_encoding
            for chess_position in response_similar_positions.hits
        ]
        similar_positions_fen_encodings_regex = "|".join(
            [f"({fen_encoding}.*)" for fen_encoding in similar_positions_fen_encodings]
        )

        query_positions_stats = es_dsl.Search(using=self.client, index="games").query(
            "nested",
            path="moves",
            query=es_dsl.Q(
                "bool",
                should=[{"prefix": {"moves.fen": fen}} for fen in similar_positions_fen_encodings],
            ),
        )
        query_positions_stats.aggs.bucket("category_fen", "nested", path="moves").bucket(
            "fen", "terms", field="moves.fen", include=similar_positions_fen_encodings_regex
        )
        query_positions_stats.aggs["category_fen"]["fen"].bucket("white", "reverse_nested").metric(
            "min_elo", "min", field="white.elo"
        ).metric("max_elo", "max", field="white.elo").metric("avg_elo", "avg", field="white.elo")
        query_positions_stats.aggs["category_fen"]["fen"].bucket("black", "reverse_nested").metric(
            "min_elo", "min", field="black.elo"
        ).metric("max_elo", "max", field="black.elo").metric("avg_elo", "avg", field="black.elo")
        query_positions_stats.aggs["category_fen"]["fen"].bucket(
            "results", "reverse_nested"
        ).metric("side_won", "terms", field="result")

        response_positions_stats = query_positions_stats.execute()
        _check_query_is_successful(query=query_positions_stats, response=response_positions_stats)

        chess_positions_pb = _es_response_to_chess_positions_pb(response_positions_stats)

        return chess_positions_pb

    def get_chess_positions_pb(self, **kwargs: Any) -> List[positions_pb2.ChessPosition]:
        match list(kwargs.keys()):
            case ["similarity_encoding"]:
                return self._get_chess_positions_by_similarity_encoding(
                    similarity_encoding=kwargs["similarity_encoding"]
                )
            case _:
                exception.log_and_raise(
                    logger,
                    exception.IllegalArgumentError,
                    f"Invalid arguments to function get_chess_positions: {kwargs}.",
                )

    def get_chess_game_pb(self, id: str) -> games_pb2.ChessGame:
        query = es_dsl.Search(using=self.client, index="games").query("match", id=id)

        response = query.execute()
        _check_query_is_successful(query=query, response=response)
        if not response.hits:
            exception.log_and_raise(
                logger, exception.NotFoundError, f"Chess game with ID {id!r} not found."
            )

        chess_game_pb = _es_response_to_chess_game_pb(response)

        return chess_game_pb

    def _get_chess_games_by_fen_encoding(self, fen_encoding: str) -> List[games_pb2.ChessGame]:
        query = es_dsl.Search(using=self.client, index="games").query(
            "nested", path="moves", query=es_dsl.Q("regexp", moves__fen=f"{fen_encoding}.*")
        )

        response = query.execute()
        _check_query_is_successful(query=query, response=response)

        chess_games_pb = _es_response_to_chess_games_pb(response)

        return chess_games_pb

    def get_chess_games_pb(self, **kwargs: Any) -> List[games_pb2.ChessGame]:
        match list(kwargs.keys()):
            case ["fen_encoding"]:
                return self._get_chess_games_by_fen_encoding(fen_encoding=kwargs["fen_encoding"])
            case _:
                err_msg = f"Invalid arguments to function get_chess_positions: {kwargs}."
                logger.error(err_msg)
                raise exception.IllegalArgumentError(err_msg)

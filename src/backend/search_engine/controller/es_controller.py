import os
import ssl
import warnings
from typing import Any, Iterable

import elasticsearch as es
import elasticsearch_dsl as es_dsl
from elasticsearch.exceptions import ElasticsearchWarning
from loguru import logger

from backend.search_engine import controller_interface
from backend.search_engine.controller import utils as es_utils
from utils import exception as exc_utils
from utils.exception import (
    ElasticSearchQueryError,
    IllegalArgumentError,
    InvalidCredentialsError,
    NotFoundError,
)
from utils.typing import JSON

warnings.simplefilter("ignore", ElasticsearchWarning)


class ESController(controller_interface.AbstractSearchEngineController):
    def __init__(self) -> None:
        url = os.getenv("SEARCH_ENGINE_URL", "https://localhost:9200")
        username = os.getenv("SEARCH_ENGINE_USERNAME")
        password = os.getenv("SEARCH_ENGINE_PASSWORD")

        if not username or not password:
            raise InvalidCredentialsError("ElasticSearch username of password not provided.")

        context = ssl.create_default_context(cafile="/Users/mihaideaconu/Documents/http_ca.crt")
        self.client = es.Elasticsearch(url, http_auth=(username, password), ssl_context=context)

        logger.info(f"Initialised Search Engine Controller at {url}.")

    def _get_chess_position_by_fen_encoding(self, fen_encoding: str) -> JSON:
        query = es_dsl.Search(using=self.client, index="positions").query(
            "match", position__fen=fen_encoding
        )

        response = query.execute()
        if not response.success():
            exc_utils.log_and_raise(
                logger,
                ElasticSearchQueryError,
                f"ElasticSearch query to retrieve a chess position failed: {query.to_dict()}.",
            )
        if not response.hits:
            exc_utils.log_and_raise(
                logger,
                NotFoundError,
                f"Chess position with FEN encoding {fen_encoding!r} not found.",
            )

        chess_position = es_utils.filter_chess_position_response(response)

        return chess_position

    def get_chess_position(self, **kwargs: Any) -> JSON:
        match list(kwargs.keys()):
            case ["fen_encoding"]:
                return self._get_chess_position_by_fen_encoding(fen_encoding=kwargs["fen_encoding"])
            case _:
                exc_utils.log_and_raise(
                    logger,
                    IllegalArgumentError,
                    f"Invalid arguments to function get_chess_position: {kwargs}.",
                )

    def _get_chess_position_stats_by_fen_encoding(self, fen_encoding: str) -> JSON:
        # Each move in the games has an associated FEN encoding of the position
        # resulting after the move is made. However, these FEN encodings have
        # additional information about the state of the game, as opposed to the
        # position FENs generated ad-hoc (e.g. castling or en-passant rights).
        # See https://www.chess.com/terms/fen-chess for more details. Because
        # of that, we query the move FEN encodings that start with the given
        # position FEN encodings.
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
        if not response.success():
            exc_utils.log_and_raise(
                logger,
                ElasticSearchQueryError,
                f"ElasticSearch query to retrieve chess position stats failed: {query.to_dict()}.",
            )

        chess_positions_stats = es_utils.filter_chess_position_stats_response(response)

        return chess_positions_stats

    def get_chess_position_stats(self, **kwargs: Any) -> JSON:
        match list(kwargs.keys()):
            case ["fen_encoding"]:
                return self._get_chess_position_stats_by_fen_encoding(
                    fen_encoding=kwargs["fen_encoding"]
                )
            case _:
                exc_utils.log_and_raise(
                    logger,
                    IllegalArgumentError,
                    f"Invalid arguments to function get_chess_position_stats: {kwargs}.",
                )

    def _get_chess_positions_by_similarity_encoding(self, similarity_encoding: str) -> JSON:
        # Querying similar positions using the similarity encoding
        query = es_dsl.Search(using=self.client, index="positions").query(
            "match", position__encoding=similarity_encoding
        )

        response = query.execute()
        if not response.success():
            exc_utils.log_and_raise(
                logger,
                ElasticSearchQueryError,
                f"ElasticSearch query to retrievea list of chess positions failed: {query.to_dict()}.",
            )

        chess_positions = es_utils.filter_chess_positions_response(response)

        return chess_positions

    def get_chess_positions(self, **kwargs: Any) -> JSON:
        match list(kwargs.keys()):
            case ["similarity_encoding"]:
                return self._get_chess_positions_by_similarity_encoding(
                    similarity_encoding=kwargs["similarity_encoding"]
                )
            case _:
                exc_utils.log_and_raise(
                    logger,
                    IllegalArgumentError,
                    f"Invalid arguments to function get_chess_positions: {kwargs}.",
                )

    def _get_chess_positions_stats_by_fen_encoding(self, fen_encodings: Iterable[str]) -> JSON:
        # Each move in the games has an associated FEN encoding of the position
        # resulting after the move is made. However, these FEN encodings have
        # additional information about the state of the game, as opposed to the
        # position FENs generated ad-hoc (e.g. castling or en-passant rights).
        # See https://www.chess.com/terms/fen-chess for more details. Because
        # of that, we query the move FEN encodings that start with the given
        # position FEN encodings.
        fen_list_regex = "|".join([f"({fen}.*)" for fen in fen_encodings])

        query = es_dsl.Search(using=self.client, index="games").query(
            "nested",
            path="moves",
            query=es_dsl.Q(
                "bool", should=[{"prefix": {"moves.fen": fen}} for fen in fen_encodings]
            ),
        )
        query.aggs.bucket("category_fen", "nested", path="moves").bucket(
            "fen", "terms", field="moves.fen", include=fen_list_regex
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
        if not response.success():
            exc_utils.log_and_raise(
                logger,
                ElasticSearchQueryError,
                f"ElasticSearch query to retrieve a list of chess position stats failed: {query.to_dict()}.",
            )

        chess_positions_stats = es_utils.filter_chess_positions_stats_response(response)

        return chess_positions_stats

    def get_chess_positions_stats(self, **kwargs: Any) -> JSON:
        match list(kwargs.keys()):
            case ["fen_encodings"]:
                return self._get_chess_positions_stats_by_fen_encoding(
                    fen_encodings=kwargs["fen_encodings"]
                )
            case _:
                exc_utils.log_and_raise(
                    logger,
                    IllegalArgumentError,
                    f"Invalid arguments to function get_chess_positions_stats: {kwargs}.",
                )

    def _get_chess_game_by_id(self, id: str) -> JSON:
        query = es_dsl.Search(using=self.client, index="games").query("match", id=id)

        response = query.execute()
        if not response.success():
            exc_utils.log_and_raise(
                logger,
                ElasticSearchQueryError,
                f"ElasticSearch query to retrieve a chess game failed: {query.to_dict()}.",
            )
        if not response.hits:
            exc_utils.log_and_raise(logger, NotFoundError, f"Chess game with ID {id!r} not found.")

        chess_game = es_utils.filter_chess_game_response(response)

        return chess_game

    def get_chess_game(self, **kwargs: Any) -> JSON:
        match list(kwargs.keys()):
            case ["id"]:
                return self._get_chess_game_by_id(id=kwargs["id"])
            case _:
                exc_utils.log_and_raise(
                    logger,
                    IllegalArgumentError,
                    f"Invalid arguments to function get_chess_game: {kwargs}.",
                )

    def _get_chess_games_by_fen_encoding(self, fen_encoding: str) -> JSON:
        fen_regex = f"{fen_encoding}.*"

        query = es_dsl.Search(using=self.client, index="games").query(
            "nested", path="moves", query=es_dsl.Q("regexp", moves__fen=fen_regex)
        )

        response = query.execute()
        if not response.success():
            exc_utils.log_and_raise(
                logger,
                ElasticSearchQueryError,
                f"ElasticSearch query to retrieve a chess games failed: {query.to_dict()}.",
            )

        chess_games = es_utils.filter_chess_games_response(response)

        return chess_games

    def get_chess_games(self, **kwargs: Any) -> JSON:
        match list(kwargs.keys()):
            case ["fen_encoding"]:
                return self._get_chess_games_by_fen_encoding(fen_encoding=kwargs["fen_encoding"])
            case _:
                exc_utils.log_and_raise(
                    logger,
                    IllegalArgumentError,
                    f"Invalid arguments to function get_chess_games: {kwargs}.",
                )

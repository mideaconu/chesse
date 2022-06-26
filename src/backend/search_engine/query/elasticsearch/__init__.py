from typing import Any

from backend.search_engine.query.elasticsearch import aggs as es_aggs
from backend.search_engine.query.elasticsearch import query as es_query
from backend.search_engine.query.elasticsearch import runtime_mappings as es_rm
from backend.search_engine.query.elasticsearch.query import (
    get_chess_game_query,
    get_chess_games_query,
    get_similar_positions_query,
)


def get_chess_position_query(
    fen_encoding: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        es_query.get_chess_positions_query([fen_encoding]),
        es_rm.get_chess_positions_runtime_mappings([fen_encoding]),
        es_aggs.get_chess_position_stats_aggs(),
    )


def get_chess_positions_query(
    fen_encodings: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        es_query.get_chess_positions_query(fen_encodings),
        es_rm.get_chess_positions_runtime_mappings(fen_encodings),
        es_aggs.get_chess_position_stats_aggs(),
    )

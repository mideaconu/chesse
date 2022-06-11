from typing import Any


def get_chess_position_query(fen_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query to request games where after one of the
    moves the position given in the FEN encoding occurs."""
    # There is a difference between the FEN encoding of a move and a position. The fen encoding
    # of a move contains additional information about the state of the game after the move is
    # made (e.g. side to move, castling, en-passant rights):
    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    # Because of that, we ignore everything that follows the position FEN encoding in the query
    return {"nested": {"path": "moves", "query": {"regexp": {"moves.fen": f"{fen_encoding}.*"}}}}


def get_similar_positions_query(similarity_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query to request positions whose similarity
    encoding best resembles the given similarity encoding."""
    return {"match": {"position.similarity_encoding": similarity_encoding}}


def get_chess_positions_query(fen_encodings: list[str]) -> dict[str, Any]:
    return {
        "nested": {
            "path": "moves",
            "query": {
                "bool": {
                    "should": [
                        {"prefix": {"moves.fen": fen_encoding}} for fen_encoding in fen_encodings
                    ]
                }
            },
        }
    }


def get_chess_game_query(id: str) -> dict[str, Any]:
    """Returns the Elasticsearch query to request a game given its ID."""
    return {"match": {"id": id}}


def get_chess_games_query(fen_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query to request the games where the position
    given by the FEN encoding occured."""
    return {"nested": {"path": "moves", "query": {"regexp": {"moves.fen": f"{fen_encoding}.*"}}}}


def _get_chess_position_aggs(include: str) -> dict[str, Any]:
    return {
        "by_fen": {
            "nested": {"path": "moves"},
            "aggs": {
                "fen": {
                    "terms": {"field": "moves.fen", "size": 1_000, "include": include},
                    "aggs": {
                        "white": {
                            "reverse_nested": {},
                            "aggs": {
                                "min_elo": {"min": {"field": "white.elo"}},
                                "max_elo": {"max": {"field": "white.elo"}},
                                "avg_elo": {"avg": {"field": "white.elo"}},
                            },
                        },
                        "black": {
                            "reverse_nested": {},
                            "aggs": {
                                "min_elo": {"min": {"field": "black.elo"}},
                                "max_elo": {"max": {"field": "black.elo"}},
                                "avg_elo": {"avg": {"field": "black.elo"}},
                            },
                        },
                        "results": {
                            "reverse_nested": {},
                            "aggs": {"side_won": {"terms": {"field": "result"}}},
                        },
                    },
                }
            },
        }
    }


def get_chess_position_aggs(fen_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch aggregations to determine the statistics of
    the chess position."""
    include_regex = f"{fen_encoding}.*"
    return _get_chess_position_aggs(include_regex)


def get_chess_positions_aggs(fen_encodings: list[str]) -> dict[str, Any]:
    """Returns the Elasticsearch aggregations to determine the statistics of
    the chess positions."""
    include_regex = "|".join([f"({fen_encoding}.*)" for fen_encoding in fen_encodings])
    return _get_chess_position_aggs(include_regex)

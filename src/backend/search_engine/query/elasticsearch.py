from typing import Any


def get_chess_position_query(fen_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query that requests games where after one of
    the moves the position given in the FEN encoding occurs, and aggregates the
    results to determine the statistics of the position."""
    # There is a difference between the FEN encoding of a move and a position. The fen encoding
    # of a move contains additional information about the state of the game after the move is
    # made (e.g. side to move, castling, en-passant rights):
    # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    # Because of that, we ignore everything that follows the position FEN encoding in the query
    return {
        "query": {
            "nested": {"path": "moves", "query": {"regexp": {"moves.fen": f"{fen_encoding}.*"}}}
        },
        "aggs": {
            "by_fen": {
                "nested": {"path": "moves"},
                "aggs": {
                    "fen": {
                        "terms": {"field": "moves.fen", "include": f"{fen_encoding}.*"},
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
        },
    }


def get_similar_positions_query(similarity_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query that requests positions whose similarity
    encoding best resembles the given similarity encoding."""
    return {"query": {"match": {"position.similarity_encoding": similarity_encoding}}}


def get_chess_positions_stats_query(fen_encodings: list[str]) -> dict[str, Any]:
    """Returns the Elasticsearch query that requests positions that match one
    of the given FEN encodings, and aggregates the results to determine the
    statistics of the positions."""
    fen_encodings_regex = "|".join([f"({fen_encoding}.*)" for fen_encoding in fen_encodings])
    return {
        "query": {
            "nested": {
                "path": "moves",
                "query": {
                    "bool": {
                        "should": [
                            {"prefix": {"moves.fen": fen_encoding}}
                            for fen_encoding in fen_encodings
                        ]
                    }
                },
            }
        },
        "aggs": {
            "by_fen": {
                "nested": {"path": "moves"},
                "aggs": {
                    "fen": {
                        "terms": {"field": "moves.fen", "include": fen_encodings_regex},
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
        },
    }


def get_game_query(id: str) -> dict[str, Any]:
    """Returns the Elasticsearch query that requests a game given its ID."""
    return {"query": {"match": {"id": id}}}


def get_games_query(fen_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query that requests the games where the
    position given by the FEN encoding occured."""
    return {
        "query": {
            "nested": {"path": "moves", "query": {"regexp": {"moves.fen": f"{fen_encoding}.*"}}}
        }
    }

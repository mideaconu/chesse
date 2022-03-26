from typing import Any, Dict, List


def get_games_query(fen_positions: List[str]) -> Dict[str, Any]:
    """"""
    fen_filters = [{"prefix": {"moves.fen": fen}} for fen in fen_positions]

    return {"query": {"nested": {"path": "moves", "query": {"bool": {"should": fen_filters}}}}}


def get_games_aggregation(fen_positions: List[str]) -> Dict[str, Any]:
    """"""
    fen_positions_regex = [f"({fen}.*)" for fen in fen_positions]
    regex = "|".join(fen_positions_regex)  # .replace("/", "\/")
    return {
        "aggs": {
            "by_fen": {
                "nested": {"path": "moves"},
                "aggs": {
                    "fen": {
                        "terms": {"field": "moves.fen", "include": regex},
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
                                "aggs": {"white_won": {"terms": {"field": "result"}}},
                            },
                        },
                    }
                },
            }
        }
    }

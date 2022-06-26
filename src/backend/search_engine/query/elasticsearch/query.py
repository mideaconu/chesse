from typing import Any


def get_similar_positions_query(similarity_encoding: str) -> dict[str, Any]:
    """Returns the Elasticsearch query to request positions whose similarity
    encoding best resembles the given similarity encoding."""
    return {"match": {"position.similarity_encoding": similarity_encoding}}


def get_chess_positions_query(fen_encodings: list[str]) -> dict[str, Any]:
    """Returns the Elasticsearch query to request a list of chess positions
    given the FEN encodings."""
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
    return {
        "nested": {
            "path": "moves",
            "query": {"bool": {"must": {"prefix": {"moves.fen": fen_encoding}}}},
        }
    }

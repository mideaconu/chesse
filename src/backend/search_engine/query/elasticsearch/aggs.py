import os
from typing import Any


def get_chess_position_stats_aggs() -> dict[str, Any]:
    """Returns the Elasticsearch aggregations to determine the statistics of
    the chess position: elo for each colour and results."""
    return {
        "positions": {
            "terms": {
                # position_fen is a runtime mapping
                "field": "position_fen",
                "size": int(os.getenv("ELASTICSEARCH_RESULT_MAX_SIZE", "10")),
            },
            "aggs": {
                "white_elo": {"stats": {"field": "white.elo"}},
                "black_elo": {"stats": {"field": "black.elo"}},
                "results": {"terms": {"field": "result"}},
            },
        }
    }

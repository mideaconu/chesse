from typing import Any


def get_chess_positions_runtime_mappings(fen_encodings: list[str]) -> dict[str, Any]:
    """Returns the Elasticsearch runtime mapping for a new attribute,
    `position_fen`, which for each game would contain all positions from
    fen_encodings that appeared in the game."""
    script = (
        """
        List position_fens = %s;
        List moves = params._source.moves;
        for (move in moves) {
            for (position_fen in position_fens) {
                if (move["fen"].startsWith(position_fen)) {
                    emit(position_fen);
                }
            }
        }
        """
        % fen_encodings
    )
    return {"position_fen": {"type": "keyword", "script": {"lang": "painless", "source": script}}}

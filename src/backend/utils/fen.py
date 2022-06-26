import chess
import structlog

from backend.tracing import trace
from backend.utils import exception

logger = structlog.get_logger()


def check_fen_encoding_is_valid(fen_encoding: str) -> None:
    """Checks if a given FEN encoding is valid.

    Args:
        fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a chess
        position. Example: the encoding for the starting position is
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

    Raises:
        InvalidFENError: If the FEN encoding is invalid, i.e. a position could
        not be established from the encoding.
    """
    span = trace.get_current_span()
    try:
        chess.Board(fen=fen_encoding)
        span.add_event("validation successful: fen encoding", {"fen_encoding": fen_encoding})
    except ValueError as e:
        raise exception.InvalidFENEncodingError(f"validation failed: {e}")

import chess
import structlog

from backend.tracing import trace
from backend.utils import exception

logger = structlog.get_logger()


def validate_fen_encoding(fen_encoding: str) -> None:
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


def validate_pagination_params(*, page_size: int, page_token: str) -> None:
    """Checks if the pagination parameters are valid.

    Args:
        page_size (int): Page size, used to limit the list of elements.
        page_token (str): Page token, used to retrieve the next elements.

    Raises:
        InvalidFENError: If one or more of the pagination parameters are
            invalid.
    """
    span = trace.get_current_span()
    if page_size < 1:
        raise exception.InvalidPaginationParamError(
            f"validation failed: page size cannot be lower than 1: {page_size}"
        )
    if page_size > 1_000:
        raise exception.InvalidPaginationParamError(
            f"validation failed: page size cannot be higher than 1,000: {page_size}"
        )
    span.add_event(
        "validation successful: pagination params",
        {"page_size": page_size, "page_token": page_token},
    )

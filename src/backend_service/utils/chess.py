import chess
from loguru import logger

from backend_service.utils import exception


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
    try:
        chess.Board(fen=fen_encoding)
        logger.debug(f"FEN encoding {fen_encoding!r} is valid.")
    except ValueError as e:
        exception.log_and_raise(
            logger,
            exception.InvalidFENEncodingError,
            {"fen_encoding": fen_encoding, "message": str(e)},
        )

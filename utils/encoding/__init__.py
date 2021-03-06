import chess
from loguru import logger

from utils import exception as exc_utils
from utils.encoding.activity_encoding import get_activity_encoding
from utils.encoding.connectivity_encoding import get_connectivity_encoding
from utils.encoding.naive_encoding import get_naive_encoding
from utils.exception import InvalidFENError


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
    except Exception as e:
        exc_utils.log_and_raise(logger, InvalidFENError, f"FEN {fen_encoding!r} is not valid: {e}")


def get_similarity_encoding(fen_encoding: str) -> str:
    """Returns a list of similarity encodings in a given chess position.

    See Ganguly, D., Leveling, J., & Jones, G. (2014). Retrieval of similar
    chess positions.

    Args:
        fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a chess
        position. Example: the encoding for the starting position is
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

    Returns:
        str: The similarity encoding of the position.
    """
    similarity_encoding = " ".join(
        (
            get_naive_encoding(fen_encoding),
            get_activity_encoding(fen_encoding),
            get_connectivity_encoding(fen_encoding),
        )
    )
    return similarity_encoding

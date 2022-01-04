from typing import Set

import chess


def _get_naive_encodings(board: chess.Board) -> Set[str]:
    """Returns the naive encodings of the chess pieces in a given chess
    position.

    See Section 5.1. Naive Encoding in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    naive_encodings = set()

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_square = chess.square_name(square)
            naive_encoding = f"{piece}{piece_square}"

            naive_encodings.add(naive_encoding)

    return naive_encodings


def get_naive_encoding(board: chess.Board) -> str:
    """Returns the naive encoding of a given chess position.

    See Section 5.1. Naive Encoding in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    return " ".join(_get_naive_encodings(board))

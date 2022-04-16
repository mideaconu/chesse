import chess

from utils import exception as exc


def get_naive_encoding(fen: str) -> str:
    """Returns a set of naive encodings of the chess pieces in a given chess
    position.

    See Section 5.1. Naive Encoding in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    try:
        board = chess.Board(fen=fen)
    except Exception as e:
        raise exc.InvalidFENError(f"FEN {fen!r} is not valid: {e}")

    naive_encodings = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_square = chess.square_name(square)
            naive_encoding = f"{piece}{piece_square}"

            naive_encodings.append(naive_encoding)

    naive_encoding = " ".join(naive_encodings)

    return naive_encoding

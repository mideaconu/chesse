from typing import List

import chess

from utils import exception as exc


def _chebyshev_distance(from_square: chess.Square, to_square: chess.Square) -> float:
    """Returns the Chebyshev distance between two squares."""
    return chess.square_distance(from_square, to_square)


def _activity_weight(from_square: chess.Square, to_square: chess.Square) -> float:
    """Returns the activity weight of two squares, rounded to the 2nd
    decimal."""
    return round(1 - (7 * _chebyshev_distance(from_square, to_square) / 64), 2)


def _get_pseudolegal_moves(board: chess.Board) -> List[chess.Move]:
    """Returns the whole list of pseudolegal moves for a board setting for both
    colours."""
    pseudolegal_moves = []

    side_to_move = board.turn
    for colour in chess.COLORS:
        board.turn = colour

        for move in board.pseudo_legal_moves:
            pseudolegal_moves.append(move)

    board.turn = side_to_move

    return pseudolegal_moves


def get_activity_encoding(fen: str) -> str:
    """Returns a list of activity encodings in a given chess position.

    See Section 5.2. Reachable Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    activity_encodings = []

    try:
        board = chess.Board(fen=fen)
    except Exception as e:
        raise exc.InvalidFENError(f"FEN {fen!r} is not valid: {e}")

    pseudolegal_moves = _get_pseudolegal_moves(board)

    for move in pseudolegal_moves:
        piece = board.piece_at(move.from_square).symbol() + chess.square_name(move.to_square)
        weight = _activity_weight(move.from_square, move.to_square)
        activity_encoding = f"{piece}|{weight}"

        activity_encodings.append(activity_encoding)

    activity_encoding = " ".join(activity_encodings)

    return activity_encoding

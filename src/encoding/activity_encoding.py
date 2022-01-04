from collections import defaultdict
from typing import List, Set

import chess


def chebyshev_distance(from_square: chess.Square, to_square: chess.Square) -> float:
    """Returns the Chebyshev distance between two squares."""
    return chess.square_distance(from_square, to_square)


def activity_weight(from_square: chess.Square, to_square: chess.Square) -> float:
    """Returns the activity weight of two squares, rounded to the 2nd
    decimal."""
    return round(1 - (7 * chebyshev_distance(from_square, to_square) / 64), 2)


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


def get_activity_encodings(board: chess.Board) -> Set[str]:
    """Returns the activity encodings in a given chess position.

    See Section 5.2. Reachable Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    activity_encodings = set()
    piece_activity = defaultdict(list)

    pseudolegal_moves = _get_pseudolegal_moves(board)

    for move in pseudolegal_moves:
        piece_activity[move.from_square].append(move.to_square)

    for from_square, to_squares in piece_activity.items():
        for to_square in to_squares:
            piece = board.piece_at(from_square).symbol() + chess.square_name(to_square)
            weight = activity_weight(from_square, to_square)
            activity_encoding = f"{piece}|{weight}"

            activity_encodings.add(activity_encoding)

    return activity_encodings


def get_activity_encoding(board: chess.Board) -> str:
    """Returns the activity encoding of a given chess position.

    See Section 5.2. Reachable Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    return " ".join(get_activity_encodings(board))

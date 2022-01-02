from collections import defaultdict
from typing import List

import chess


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


def get_chebyshev_distance(from_square: chess.Square, to_square: chess.Square) -> float:
    """Returns the Chebyshev distance between two squares."""
    return chess.square_distance(from_square, to_square)


def get_activity_weight(from_square: chess.Square, to_square: chess.Square) -> float:
    """Returns the activity weight of two squares."""
    return 1 - (7 * get_chebyshev_distance(from_square, to_square) / 64)


def get_naive_encoding(board: chess.Board) -> str:
    """Returns the naive encoding of a given chess position.

    See Section 5.1. Naive Encoding in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    naive_encoding = ""

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            naive_encoding += f"{piece}{chess.square_name(square)} "

    return naive_encoding.strip()


def get_activity_encoding(board: chess.Board) -> str:
    """Returns the activity encoding of a given chess position.

    See Section 5.2. Reachable Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    activity_encoding = ""
    piece_activity = defaultdict(list)

    pseudolegal_moves = _get_pseudolegal_moves(board)
    for move in pseudolegal_moves:
        piece_activity[move.from_square].append(move.to_square)

    for from_square, to_squares in piece_activity.items():
        for to_square in to_squares:
            piece = str(board.piece_at(from_square)) + chess.square_name(to_square)
            weight = round(get_activity_weight(from_square, to_square), 2)

            activity_encoding += f"{piece}|{weight} "

    return activity_encoding.strip()


def get_similarity_encoding(fen: str):
    """Returns the similarity encoding of a given chess position.

    See Section 5. Similarity Computation in Ganguly, D., Leveling, J.,
    & Jones, G. (2014). Retrieval of similar chess positions.
    """
    board = chess.Board(fen=fen)

    naive_encoding = get_naive_encoding(board)
    activity_encoding = get_activity_encoding(board)

    similarity_encoding = f"{naive_encoding}\n{activity_encoding}"

    return similarity_encoding


if __name__ == "__main__":
    print(get_similarity_encoding("r1bk2r1/p1p5/1pqp3p/5Bp1/7Q/8/P2N2PP/3KR3 w - g6"))

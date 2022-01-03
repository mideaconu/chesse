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
            piece_square = chess.square_name(square)
            naive_encoding += f"{piece}{piece_square} "

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


def get_connectivity_encoding(board: chess.Board, connection: str) -> str:
    """Returns the attack encoding of a given chess position.

    See Section 5.3. Connectivity between the pieces in Ganguly, D.,
    Leveling, J., & Jones, G. (2014). Retrieval of similar chess
    positions.
    """
    supported_connections = {"attack", "defense"}
    if connection not in supported_connections:
        raise ValueError(
            f"Connection not supported: {connection}. Supported connections: {supported_connections}."
        )

    attack_encoding = ""

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            attacked_squares = board.attacks(square)
            for attacked_square in attacked_squares:
                attacked_piece = board.piece_at(attacked_square)

                if connection == "attack":
                    if attacked_piece and piece.color != attacked_piece.color:
                        attacked_piece_square = chess.square_name(attacked_square)
                        attack_encoding += f"{piece}>{attacked_piece}{attacked_piece_square} "
                elif connection == "defense":
                    if attacked_piece and piece.color == attacked_piece.color:
                        attacked_piece_square = chess.square_name(attacked_square)
                        attack_encoding += f"{piece}<{attacked_piece}{attacked_piece_square} "

    return attack_encoding.strip()


def get_similarity_encoding(fen: str):
    """Returns the similarity encoding of a given chess position.

    See Section 5. Similarity Computation in Ganguly, D., Leveling, J.,
    & Jones, G. (2014). Retrieval of similar chess positions.
    """
    board = chess.Board(fen=fen)
    print(board)

    naive_encoding = get_naive_encoding(board)
    activity_encoding = get_activity_encoding(board)
    attack_encoding = get_connectivity_encoding(board, connection="attack")
    defense_encoding = get_connectivity_encoding(board, connection="defense")

    similarity_encoding = (
        f"{naive_encoding}\n{activity_encoding}\n{attack_encoding}\n{defense_encoding}"
    )

    return similarity_encoding


if __name__ == "__main__":
    print(get_similarity_encoding("r1bk2r1/p1p5/1pqp3p/5Bp1/7Q/8/P2N2PP/3KR3 w - g6"))

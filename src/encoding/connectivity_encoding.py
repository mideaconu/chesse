import copy
from typing import Set

import chess


def get_attack_encodings(piece: chess.Piece, square: chess.Square, board: chess.Board) -> Set[str]:
    """Returns the attack encodings of a given chess position.

    See Section 5.3.1 Attack Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    attack_encodings = set()

    attacked_squares = board.attacks(square)
    for attacked_square in attacked_squares:
        attacked_piece = board.piece_at(attacked_square)

        if attacked_piece and piece.color != attacked_piece.color:
            attacked_piece_square = chess.square_name(attacked_square)
            attack_encoding = f"{piece}>{attacked_piece}{attacked_piece_square}"

            attack_encodings.add(attack_encoding)

    return attack_encodings


def get_defense_encodings(piece: chess.Piece, square: chess.Square, board: chess.Board) -> Set[str]:
    """Returns the defense encodings of a given chess position.

    See Section 5.3.2 Defense Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    defense_encodings = set()

    attacked_squares = board.attacks(square)
    for attacked_square in attacked_squares:
        attacked_piece = board.piece_at(attacked_square)

        if attacked_piece and piece.color == attacked_piece.color:
            attacked_piece_square = chess.square_name(attacked_square)
            defense_encoding = f"{piece}<{attacked_piece}{attacked_piece_square}"

            defense_encodings.add(defense_encoding)

    return defense_encodings


def get_ray_attack_encodings(
    piece: chess.Piece, square: chess.Square, board: chess.Board
) -> Set[str]:
    """Returns the ray attack encodings of a given chess position.

    See Section 5.3.3 Ray-Attack Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    ray_attack_encodings = set()
    board_copy = copy.deepcopy(board)

    attacked_squares = board_copy.attacks(square)
    initial_attacked_squares = copy.deepcopy(attacked_squares)

    while attacked_squares:
        current_attacked_square = attacked_squares.pop()

        attacked_piece = board_copy.piece_at(current_attacked_square)
        attacked_piece_square = chess.square_name(current_attacked_square)

        if attacked_piece:
            if piece.color != attacked_piece.color:
                ray_attack_encoding = f"{piece}={attacked_piece}{attacked_piece_square}"
                ray_attack_encodings.add(ray_attack_encoding)

            board_copy.remove_piece_at(current_attacked_square)
            attacked_squares |= board_copy.attacks(square) - initial_attacked_squares

    return ray_attack_encodings


def get_connectivity_encodings(board: chess.Board, connection: str) -> str:
    """Returns the attack encodings of a given chess position.

    See Section 5.3. Connectivity between the pieces in Ganguly, D.,
    Leveling, J., & Jones, G. (2014). Retrieval of similar chess
    positions.
    """
    supported_connections = {"ray-attack", "attack", "defense"}
    if connection not in supported_connections:
        raise ValueError(
            f"Connection not supported: {connection}. Supported connections: {supported_connections}."
        )

    connect_encodings = set()

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if connection == "attack":
                connect_encodings |= get_attack_encodings(piece, square, board)
            elif connection == "defense":
                connect_encodings |= get_defense_encodings(piece, square, board)
            elif connection == "ray-attack":
                connect_encodings |= get_ray_attack_encodings(piece, square, board)

    return connect_encodings


def get_connectivity_encoding(board: chess.Board, connection: str) -> str:
    """Returns the attack encoding of a given chess position.

    See Section 5.3. Connectivity between the pieces in Ganguly, D.,
    Leveling, J., & Jones, G. (2014). Retrieval of similar chess
    positions.
    """
    return " ".join(get_connectivity_encodings(board, connection))

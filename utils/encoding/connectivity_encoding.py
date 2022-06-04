import copy
import itertools
from typing import List

import chess


def _get_attack_encodings(
    piece: chess.Piece, square: chess.Square, board: chess.Board
) -> List[str]:
    """Returns a set of attack encodings of a given chess position."""
    attack_encodings = []

    attacked_squares = board.attacks(square)
    for attacked_square in attacked_squares:
        attacked_piece = board.piece_at(attacked_square)

        if attacked_piece and piece.color != attacked_piece.color:
            attacked_piece_square = chess.square_name(attacked_square)
            attack_encoding = f"{piece}>{attacked_piece}{attacked_piece_square}"

            attack_encodings.append(attack_encoding)

    return attack_encodings


def _get_defense_encodings(
    piece: chess.Piece, square: chess.Square, board: chess.Board
) -> List[str]:
    """Returns a set of defense encodings of a given chess position."""
    defense_encodings = []

    attacked_squares = board.attacks(square)
    for attacked_square in attacked_squares:
        attacked_piece = board.piece_at(attacked_square)

        if attacked_piece and piece.color == attacked_piece.color:
            attacked_piece_square = chess.square_name(attacked_square)
            defense_encoding = f"{piece}<{attacked_piece}{attacked_piece_square}"

            defense_encodings.append(defense_encoding)

    return defense_encodings


def _get_ray_attack_encodings(
    piece: chess.Piece, square: chess.Square, board: chess.Board
) -> List[str]:
    """Returns a set of ray attack encodings of a given chess position."""
    ray_attack_encodings = []
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
                ray_attack_encodings.append(ray_attack_encoding)

            board_copy.remove_piece_at(current_attacked_square)
            attacked_squares |= board_copy.attacks(square) - initial_attacked_squares

    return ray_attack_encodings


def get_connectivity_encoding(fen: str) -> str:
    """Returns the connectivity encoding of a given chess position.

    See Section 5.3. Connectivity between the pieces in Ganguly, D.,
    Leveling, J., & Jones, G. (2014). Retrieval of similar chess
    positions.

    Args:
        fen (str): Forsyth-Edwards Notation (FEN) encoding of a chess
        position. Example: the encoding for the starting position is
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

    Raises:
        ValueError: If the FEN encoding is invalid.

    Returns:
        str: Connectivity encoding.
    """
    board = chess.Board(fen=fen)

    connectivity_encodings = []
    attack_encodings = []
    defense_encodings = []
    ray_attack_encodings = []
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            attack_encodings.extend(_get_attack_encodings(piece, square, board))
            defense_encodings.extend(_get_defense_encodings(piece, square, board))
            ray_attack_encodings.extend(_get_ray_attack_encodings(piece, square, board))

    connectivity_encodings = list(
        itertools.chain(attack_encodings, defense_encodings, ray_attack_encodings)
    )

    connectivity_encoding = " ".join(connectivity_encodings)

    return connectivity_encoding

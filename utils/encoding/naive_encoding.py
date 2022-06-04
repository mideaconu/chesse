import chess


def get_naive_encoding(fen: str) -> str:
    """Returns the naive encoding of a given chessposition.

    See Section 5.1. Naive Encoding in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.

    Args:
        fen (str): Forsyth-Edwards Notation (FEN) encoding of a chess
        position. Example: the encoding for the starting position is
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

    Raises:
        ValueError: If the FEN encoding is invalid.

    Returns:
        str: Naive encoding.
    """
    board = chess.Board(fen=fen)

    naive_encodings = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_square = chess.square_name(square)
            naive_encoding = f"{piece}{piece_square}"

            naive_encodings.append(naive_encoding)

    naive_encoding = " ".join(naive_encodings)

    return naive_encoding

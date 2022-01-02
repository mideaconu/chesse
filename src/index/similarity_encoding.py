import chess


def get_naive_encoding(board: chess.Board) -> str:
    """Returns the naive encoding of a given chess position.

    The naive encoding represents the set of pieces availale on the given
    board, in the format <PIECE><FILE><RANK>:
        - <PIECE> is a letter corresponding to the piece type: q for queen,
            k for king, b for bishon, n for knight, r for rook, and p for pawn.
            To distinguish between colours, uppercase letters are being used
            for white and lowercase letters for black.
        - <FILE> is the file the piece is on, from a to h.
        - <RANK> is the rank the piece is on, from 1 to 8.

    Example: Rc8 is the white rook on c8, ph7 is the black pawn on h7.
    """
    naive_encoding = ""

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            naive_encoding += f"{piece}{chess.square_name(square)} "

    return naive_encoding.strip()


def get_similarity_encoding(fen: str):
    similarity_encoding = ""

    board = chess.Board(fen=fen)

    similarity_encoding += get_naive_encoding(board)

    return similarity_encoding


if __name__ == "__main__":
    print(
        get_similarity_encoding(
            "r1b2rk1/1pq1ppbp/p2p1np1/3N4/1P2P3/P2B4/2P1NPPP/1R1Q1RK1 b - -"
        )
    )

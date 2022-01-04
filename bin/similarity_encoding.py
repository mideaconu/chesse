import chess

from src.encoding import activity_encoding, connectivity_encoding, naive_encoding


def get_similarity_encoding(fen: str):
    """Returns the similarity encoding of a given chess position.

    See Section 5. Similarity Computation in Ganguly, D., Leveling, J.,
    & Jones, G. (2014). Retrieval of similar chess positions.
    """
    board = chess.Board(fen=fen)
    print(board)

    similarity_encoding = (
        f"{naive_encoding.get_naive_encoding(board)}\n"
        f"{activity_encoding.get_activity_encoding(board)}\n"
        f"{connectivity_encoding.get_connectivity_encoding(board, 'attack')}\n"
        f"{connectivity_encoding.get_connectivity_encoding(board, 'defense')}\n"
        f"{connectivity_encoding.get_connectivity_encoding(board, 'ray-attack')}"
    )

    return similarity_encoding


if __name__ == "__main__":
    print(get_similarity_encoding("2kr4/1p1qpp2/p1n1b1p1/2pN1nP1/5N2/1P1PPQ2/PKP2P2/3R3B b - -"))

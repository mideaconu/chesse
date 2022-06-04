from utils.encoding.activity_encoding import get_activity_encoding
from utils.encoding.connectivity_encoding import get_connectivity_encoding
from utils.encoding.naive_encoding import get_naive_encoding


def get_similarity_encoding(fen_encoding: str) -> str:
    """Returns a list of similarity encodings in a given chess position.

    See Ganguly, D., Leveling, J., & Jones, G. (2014). Retrieval of similar
    chess positions.

    Args:
        fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a chess
        position. Example: the encoding for the starting position is
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

    Raises:
        ValueError: If the FEN encoding is invalid.

    Returns:
        str: Similarity encoding.
    """
    similarity_encoding = " ".join(
        (
            get_naive_encoding(fen_encoding),
            get_activity_encoding(fen_encoding),
            get_connectivity_encoding(fen_encoding),
        )
    )
    return similarity_encoding

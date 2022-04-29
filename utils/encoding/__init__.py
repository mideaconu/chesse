from utils.encoding.activity_encoding import get_activity_encoding
from utils.encoding.connectivity_encoding import get_connectivity_encoding
from utils.encoding.naive_encoding import get_naive_encoding


def get_similarity_encoding(fen: str) -> str:
    """Returns a list of similarity encodings in a given chess position.

    See Section 5.2. Reachable Squares in Ganguly, D., Leveling, J., &
    Jones, G. (2014). Retrieval of similar chess positions.
    """
    similarity_encoding = " ".join(
        (get_naive_encoding(fen), get_activity_encoding(fen), get_connectivity_encoding(fen))
    )
    return similarity_encoding

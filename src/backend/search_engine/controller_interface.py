from abc import abstractmethod
from typing import Iterable

from utils import meta
from utils.typing import JSON


class AbstractSearchEngineController(metaclass=meta.SingletonABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_similar_positions(self, position_encoding: str) -> JSON:
        """Retrieve positions that have a similarity encoding similar to the
        position_encoding in the data store.

        Args:
            position_encoding (str): Similarity encoding of the query position.

        Returns:
            JSON: A list of JSON objects of the following structure (sorted by
            the similarity_score):
                - fen (str): FEN encoding of the similar position.
                - similarity_score (float): A score indicating how similar the
                    position is to the query position.
        """
        raise NotImplementedError

    @abstractmethod
    def get_positions_stats(self, fen_list: Iterable[str]) -> JSON:
        """Retrieve positions stats for each of the query positions in the
        fen_list.

        Args:
            fen_list (Iterable[str]): List of FEN encodings for the query
            positions.

        Returns:
            JSON: A JSON object that specifies a set of games stats for each
            query position:
                - nr_games (int): Number of games the positions appears in.
                - rating (JSON): Stats for the rating of the players that
                played a game in which the query position occured.
                    - min (int): Lowest-rated player.
                    - avg (float): Average rating of the platers.
                    - max (int): Highest-rated player.
                - results (JSON): Results stats for the games where the query
                position occured.
                    - white (float): Percentage of wins by white.
                    - draw (float): Percentage of draws.
                    - black (float): Percentage of wins by black.
        """
        raise NotImplementedError

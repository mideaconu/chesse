from abc import abstractmethod
from typing import Any, List

from chesse.v1alpha1 import games_pb2, positions_pb2

from backend.utils import meta


class AbstractSearchEngineController(metaclass=meta.SingletonABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get_chess_position_pb(self, fen_encoding: str) -> positions_pb2.ChessPosition:
        """Returns a chess position.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.

        Returns:
            positions_pb2.ChessPosition: Chess position pb object.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chess_positions_pb(self, **kwargs: Any) -> List[positions_pb2.ChessPosition]:
        """Returns a list of chess positions. One of the following sets of
        arguments can be passed to the function:

        - (similarity_encoding): Returns a list of chess positions similar to
        the position for which the encoding is given. The returned
        positions are ordered by similarity.

        Args:
            similarity_encoding (str): The encoding of the chess position that
            similar positions should be returned for. See Ganguly, D.,
            Leveling, J., & Jones, G. (2014). Retrieval of similar chess
            positions.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.

        Returns:
            List[positions_pb2.ChessPosition]: List of chess position pb
            objects.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chess_game_pb(self, id: str) -> games_pb2.ChessGame:
        """Returns a chess game.

        Args:
            id (str): Chess game unique identifier.

        Returns:
            games_pb2.ChessGame: Chess game pb object.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chess_games_pb(self, **kwargs) -> List[games_pb2.ChessGame]:
        """Returns a collection of chess games. One of the following sets of
        arguments can be passed to the function:

        - (fen_encoding): Returns the chess games for the position given as the
        FEN encoding.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.

        Returns:
            List[games_pb2.ChessGame]: List of chess games pb objects.
        """
        raise NotImplementedError()

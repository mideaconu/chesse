from abc import abstractmethod

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
    def get_chess_positions_pb(
        self, similarity_encoding: str, page_size: int, page_token: str
    ) -> tuple[list[positions_pb2.ChessPosition], int, str]:
        """Returns a list of chess positions.

        Args:
            similarity_encoding (str): The encoding of the chess position that
            similar positions should be returned for. See Ganguly, D.,
            Leveling, J., & Jones, G. (2014). Retrieval of similar chess
            positions.
            page_size (str): The maximum number of chess positions to return.
            page_token (str): Pointer to a specific chess position where to
            start from in the list.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.

        Returns:
            tuple
                list[positions_pb2.ChessPosition]: List of chess position pb
                objects.
                int: The total number of elements in the returned list.
                str: The token for the next batch of elements.
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
    def get_chess_games_pb(
        self, fen_encoding: str, page_size: int, page_token: str
    ) -> tuple[list[games_pb2.ChessGame], int, str]:
        """Returns a collection of chess games.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.
            page_size (str): The maximum number of chess games to return.
            page_token (str): Pointer to a specific chess game where to start
            from in the list.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.

        Returns:
            tuple
                list[positions_pb2.ChessGame]: List of chess game pb objects.
                int: The total number of elements in the returned list.
                str: The token for the next batch of elements.
        """
        raise NotImplementedError()

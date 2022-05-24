from abc import abstractmethod
from typing import Any

from utils import meta
from utils.typing import JSON


class AbstractSearchEngineController(metaclass=meta.SingletonABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_chess_position(self, **kwargs: Any) -> JSON:
        """Returns a chess position. One of the following sets of arguments can
        be passed to the function:

        - (fen_encoding): Returns a chess position that matches the given FEN
        encoding.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.
            NotFoundError: If the position could not be found.

        Returns:
            JSON: A JSON object of the following structure:
            - fen_encoding (str): FEN encoding of the chess position.
            - similarity_encoding (str): Similarity encoding of the chess
            position.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chess_position_stats(self, **kwargs: Any) -> JSON:
        """Returns a chess position's statistics. One of the following sets of
        arguments can be passed to the function:

        - (fen_encoding): Returns the chess position statistics for the
        position given as the FEN encoding.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.
            NotFoundError: If the position could not be found.

        Returns:
            JSON: A JSON object that specifies the game statistics:
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
        raise NotImplementedError()

    @abstractmethod
    def get_chess_positions(self, **kwargs: Any) -> JSON:
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
            JSON: A list of JSON objects of the following structure (sorted by
            the similarity_score):
            - fen_encoding (str): FEN encoding of the similar position.
            - similarity_encoding (str): Similarity encoding of the similar
            position.
            - similarity_score (float): A score indicating how similar
            the position is to the query position.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chess_positions_stats(self, **kwargs: Any) -> JSON:
        """Returns a collection of position stats. One of the following sets of
        arguments can be passed to the function:

        - (fen_encodings): Returns a list of chess position stats for each of
            the positions given as FEN encodings.

        Args:
            fen_encodings (Iterable[str]): Forsyth-Edwards Notation (FEN)
            encodings of a collection of chess positions. Example: the encoding
            for the starting position and the same position with only kings on
            the board is [rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR,
            4k3/8/8/8/8/8/8/4K3].

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.

        Returns:
            JSON: A JSON object that specifies a set of games stats for each
            position:
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
        raise NotImplementedError()

    @abstractmethod
    def get_chess_game(self, **kwargs) -> JSON:
        """Returns a chess game. One of the following sets of arguments can be
        passed to the function:

        - (id): Returns the chess game that matches the given game ID.

        Args:
            id (str): Chess game unique identifier.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.
            NotFoundError: If the game could not be found.

        Returns:
            JSON: A JSON object of the following structure:
            - id (str): Chess game ID.
            - context (JSON): Context in which the game was played.
                - event (str): Event that the game was played in.
                - date (str): Date of the game.
                - site (str): Site that the game can be accessed at.
                - round (float): Round number.
            - white (JSON): Side with the white pieces.
                - name (str): Name of the player.
                - elo (int): Elo rating of the player.
            - black (JSON): Side with the black pieces.
                - name (str): Name of the player.
                - elo (int): Elo rating of the player.
            - moves (JSON): List of moves made in the game.
                - uci (str): Universal Chess Interface (UCI) encoding of the
                move.
                - san (str): Simplified Algebraic Notation (SAM) encoding of
                the move.
                - fen (str): Forsyth-Edwards Notation (FEN) encoding of the
                position after the move has been made.
            - result (float): Game result: 1 if white won, 0.5 for draw, 0 if
            black won.
        }
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chess_games(self, **kwargs) -> JSON:
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
            JSON: A collection of JSON objects of the following structure:
            - id (str): Chess game ID.
            - context (JSON): Context in which the game was played.
                - event (str): Event that the game was played in.
                - date (str): Date of the game.
                - site (str): Site that the game can be accessed at.
                - round (float): Round number.
            - white (JSON): Side with the white pieces.
                - name (str): Name of the player.
                - elo (int): Elo rating of the player.
            - black (JSON): Side with the black pieces.
                - name (str): Name of the player.
                - elo (int): Elo rating of the player.
            - moves (JSON): List of moves made in the game.
                - uci (str): Universal Chess Interface (UCI) encoding of the
                move.
                - san (str): Simplified Algebraic Notation (SAM) encoding of
                the move.
                - fen (str): Forsyth-Edwards Notation (FEN) encoding of the
                position after the move has been made.
            - result (float): Game result: 1 if white won, 0.5 for draw, 0 if
            black won.
        """
        raise NotImplementedError()

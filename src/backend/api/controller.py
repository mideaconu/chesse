from loguru import logger

from backend import factory
from utils import encoding
from utils import encoding as encoding_utils
from utils.typing import JSON


class CheSSEBackendController:
    def __init__(self) -> None:
        self.search_engine_controller = factory.CheSSEBackendFactory.get_search_engine_controller()

    def get_chess_position(self, fen_encoding: str) -> JSON:
        """Returns a chess position JSON object.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Raises:
            InternalServerError: If there is a server side error raised upon
            making the request.
            InvalidFENError: If the FEN encoding is invalid.
            NotFoundError: If the position could not be found.

        Returns:
            JSON: A JSON object of the following structure:
            - fen_encoding (str): FEN encoding of the position.
            - stats (JSON): Position statistics:
                - nr_games (int): Number of games the positions appears
                in.
                - rating (JSON): Stats for the rating of the players
                that played a game in which the query position occured.
                    - min (int): Lowest-rated player.
                    - avg (float): Average rating of the platers.
                    - max (int): Highest-rated player.
                - results (JSON): Results stats for the games where the
                query position occured.
                    - white (float): Percentage of wins by white.
                    - draw (float): Percentage of draws.
                    - black (float): Percentage of wins by black.
        """
        encoding_utils.check_fen_encoding_is_valid(fen_encoding)

        chess_position = self.search_engine_controller.get_chess_position(fen_encoding=fen_encoding)

        chess_position_stats = self.search_engine_controller.get_chess_position_stats(
            fen_encoding=fen_encoding
        )
        chess_position["stats"] = chess_position_stats

        return chess_position

    def get_chess_positions(self, fen_encoding: str) -> JSON:
        """Returns a list of chess position JSON objects.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Returns:
            JSON: A list of JSON objects of the following structure sorted by
            similarity score:
            - fen_encoding (str): FEN encoding of the position.
            - stats (JSON): Position statistics:
                - nr_games (int): Number of games the positions appears
                in.
                - rating (JSON): Stats for the rating of the players
                that played a game in which the query position occured.
                    - min (int): Lowest-rated player.
                    - avg (float): Average rating of the platers.
                    - max (int): Highest-rated player.
                - results (JSON): Results stats for the games where the
                query position occured.
                    - white (float): Percentage of wins by white.
                    - draw (float): Percentage of draws.
                    - black (float): Percentage of wins by black.
        """
        encoding_utils.check_fen_encoding_is_valid(fen_encoding)

        similarity_encoding = encoding.get_similarity_encoding(fen_encoding)
        logger.debug(f"Similarity encoding for position {fen_encoding}: {similarity_encoding}")

        chess_positions = self.search_engine_controller.get_chess_positions(
            similarity_encoding=similarity_encoding
        )

        fen_encodings = [position["fen_encoding"] for position in chess_positions]
        postion_stats = self.search_engine_controller.get_chess_positions_stats(
            fen_encodings=fen_encodings
        )

        for position in chess_positions:
            position["stats"] = postion_stats[position["fen_encoding"]]

        return chess_positions

    def get_chess_game(self, id: str) -> JSON:
        """Returns a chess game JSON object.

        Args:
            id (str): Chess game unique identifier.

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
        """
        chess_game = self.search_engine_controller.get_chess_game(id=id)

        return chess_game

    def get_chess_games(self, fen_encoding: str) -> JSON:
        """Returns a list of chess games JSON object.

        Args:
            fen_encoding (str): Forsyth-Edwards Notation (FEN) encoding of a
            chess position. Example: the encoding for the starting position is
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR.

        Returns:
            JSON: A list of JSON objects of the following structure:
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
        chess_games = self.search_engine_controller.get_chess_games(fen_encoding=fen_encoding)

        return chess_games

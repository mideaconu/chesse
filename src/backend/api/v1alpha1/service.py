import grpc
from chesse_backend_api.v1alpha1 import chesse_pb2
from chesse_backend_api.v1alpha1.chesse_pb2_grpc import CheSSEBackendServiceServicer
from google.protobuf import json_format
from loguru import logger

from backend.api import controller
from backend.utils import pb2 as pb2_utils
from utils import exception as exc_utils
from utils.exception import CheSSEBackendServerError


class CheSSEBackendService(CheSSEBackendServiceServicer):
    def __init__(self) -> None:
        self.chesse_backend_controller = controller.CheSSEBackendController()

    def GetChessPosition(
        self, request: chesse_pb2.GetChessPositionRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetChessPositionResponse:
        """Retrieves a chess position."""
        logger.info(f"GetChessPositionRequest: {json_format.MessageToDict(request)}")

        response = chesse_pb2.GetChessPositionResponse()

        try:
            chess_position_json = self.chesse_backend_controller.get_chess_position(
                fen_encoding=request.fen_encoding
            )
            logger.debug(
                f"Chess position retrieved with FEN encoding {request.fen_encoding}: "
                f"{chess_position_json}"
            )

            chess_position_pb2 = pb2_utils.convert_json_to_pb2(
                chess_position_json=chess_position_json
            )
            response = chesse_pb2.GetChessPositionResponse(position=chess_position_pb2)
        except CheSSEBackendServerError as e:
            exc_utils.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.info(f"GetChessPositionResponse: {json_format.MessageToDict(response)}")

        return response

    def GetChessPositions(
        self, request: chesse_pb2.GetChessPositionsRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetChessPositionsResponse:
        """Retrieves a list of chess positions."""
        logger.info(f"GetChessPositionsRequest: {json_format.MessageToDict(request)}")

        response = chesse_pb2.GetChessPositionsResponse()

        try:
            chess_positions_json = self.chesse_backend_controller.get_chess_positions(
                fen_encoding=request.fen_encoding
            )
            logger.debug(
                f"Number of chess positions retrieved similar to position {request.fen_encoding}: "
                f"{len(chess_positions_json)}"
            )

            chess_positions_pb2 = pb2_utils.convert_json_to_pb2(
                chess_positions_json=chess_positions_json
            )
            response = chesse_pb2.GetChessPositionsResponse(positions=chess_positions_pb2)
        except CheSSEBackendServerError as e:
            exc_utils.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.info(f"GetChessPositionsResponse: {json_format.MessageToDict(response)}")

        return response

    def GetChessGame(
        self, request: chesse_pb2.GetChessGameRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetChessGameResponse:
        """Retrieves a chess game."""
        logger.info(f"GetChessGameRequest: {json_format.MessageToDict(request)}")

        response = chesse_pb2.GetChessGameRequest()

        try:
            chess_game_json = self.chesse_backend_controller.get_chess_game(id=request.game_id)
            logger.debug(f"Chess game retrieved with ID {request.game_id}: {chess_game_json}")

            chess_game_pb2 = pb2_utils.convert_json_to_pb2(chess_game_json=chess_game_json)
            response = chesse_pb2.GetChessGameResponse(game=chess_game_pb2)
        except CheSSEBackendServerError as e:
            exc_utils.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.info(f"GetChessGameResponse: {json_format.MessageToDict(response)}")

        return response

    def GetChessGames(
        self, request: chesse_pb2.GetChessGamesRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetChessGamesResponse:
        """Retrieves a list of chess games."""
        logger.info(f"GetChessGamesRequest: {json_format.MessageToDict(request)}")

        response = chesse_pb2.GetChessGamesRequest()

        try:
            chess_games_json = self.chesse_backend_controller.get_chess_games(
                fen_encoding=request.fen_encoding
            )
            logger.debug(
                f"Chess games retrieved with FEN encoding {request.fen_encoding}: "
                f"{chess_games_json}"
            )

            chess_games_pb2 = pb2_utils.convert_json_to_pb2(chess_games_json=chess_games_json)
            response = chesse_pb2.GetChessGamesResponse(games=chess_games_pb2)
        except CheSSEBackendServerError as e:
            exc_utils.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.info(f"GetChessGamesResponse: {json_format.MessageToDict(response)}")

        return response

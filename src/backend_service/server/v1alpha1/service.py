import os
import sys

import grpc
from chesse.v1alpha1 import backend_service_pb2, services_pb2_grpc
from google.protobuf import json_format
from loguru import logger

from backend_service.search_engine import factory
from backend_service.utils import encoding, exception, meta


class BackendService(services_pb2_grpc.BackendServiceServicer, metaclass=meta.Singleton):
    def __init__(self) -> None:
        try:
            self.search_engine_controller = factory.SearchEngineFactory.get_controller()
        except (ValueError, exception.InvalidCredentialsError) as e:
            logger.error(f"Error initialising the search engine controller: {e}")
            sys.exit(os.EX_CONFIG)

    def GetChessPosition(
        self, request: backend_service_pb2.GetChessPositionRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessPositionResponse:
        logger.debug(f"GetChessPositionRequest: {json_format.MessageToDict(request)}")

        response = backend_service_pb2.GetChessPositionResponse()

        try:
            encoding.check_fen_encoding_is_valid(request.fen_encoding)

            chess_position_pb = self.search_engine_controller.get_chess_position_pb(
                request.fen_encoding
            )
            response = backend_service_pb2.GetChessPositionResponse(position=chess_position_pb)
        except exception.BackendServerError as e:
            exception.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.debug(f"GetChessPositionResponse: {json_format.MessageToDict(response)}")

        return response

    def GetChessPositions(
        self, request: backend_service_pb2.GetChessPositionsRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessPositionsResponse:
        logger.debug(f"GetChessPositionsRequest: {json_format.MessageToDict(request)}")

        response = backend_service_pb2.GetChessPositionsResponse()

        try:
            encoding.check_fen_encoding_is_valid(request.fen_encoding)

            similarity_encoding = encoding.get_similarity_encoding(request.fen_encoding)
            logger.debug(
                f"Similarity encoding for position {request.fen_encoding}: {similarity_encoding}"
            )

            chess_positions_pb = self.search_engine_controller.get_chess_positions_pb(
                similarity_encoding=similarity_encoding
            )
            response = backend_service_pb2.GetChessPositionsResponse(positions=chess_positions_pb)
        except exception.BackendServerError as e:
            exception.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.debug(f"GetChessPositionsResponse: {json_format.MessageToDict(response)}")

        return response

    def GetChessGame(
        self, request: backend_service_pb2.GetChessGameRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessGameResponse:
        logger.debug(f"GetChessGameRequest: {json_format.MessageToDict(request)}")

        response = backend_service_pb2.GetChessGameRequest()

        try:
            chess_game_pb = self.search_engine_controller.get_chess_game_pb(request.game_id)
            response = backend_service_pb2.GetChessGameResponse(game=chess_game_pb)
        except exception.BackendServerError as e:
            exception.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.debug(f"GetChessGameResponse: {json_format.MessageToDict(response)}")

        return response

    def GetChessGames(
        self, request: backend_service_pb2.GetChessGamesRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessGamesResponse:
        logger.debug(f"GetChessGamesRequest: {json_format.MessageToDict(request)}")

        response = backend_service_pb2.GetChessGamesRequest()

        try:
            chess_games_pb = self.search_engine_controller.get_chess_games_pb(
                fen_encoding=request.fen_encoding
            )
            response = backend_service_pb2.GetChessGamesResponse(games=chess_games_pb)
        except exception.BackendServerError as e:
            exception.set_error_context(context, details=str(e), status_code=e.status_code)

        logger.debug(f"GetChessGamesResponse: {json_format.MessageToDict(response)}")

        return response

import os
import sys

import grpc
from chesse.v1alpha1 import backend_service_pb2, services_pb2_grpc
from loguru import logger

import encoding
from backend.search_engine import factory
from backend.utils import exception
from backend.utils import fen as chess_utils
from backend.utils import meta


class BackendService(services_pb2_grpc.BackendServiceServicer, metaclass=meta.Singleton):
    def __init__(self) -> None:
        try:
            self.search_engine_ctrl = factory.SearchEngineFactory.get_controller()
        except (ValueError, exception.InvalidCredentialsError) as e:
            logger.critical(f"Error initialising the search engine controller: {e}")
            sys.exit(os.EX_CONFIG)

    def GetChessPosition(
        self, request: backend_service_pb2.GetChessPositionRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessPositionResponse:
        chess_utils.check_fen_encoding_is_valid(request.fen_encoding)

        chess_position_pb = self.search_engine_ctrl.get_chess_position_pb(request.fen_encoding)
        response = backend_service_pb2.GetChessPositionResponse(position=chess_position_pb)

        return response

    def GetChessPositions(
        self, request: backend_service_pb2.GetChessPositionsRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessPositionsResponse:
        chess_utils.check_fen_encoding_is_valid(request.fen_encoding)

        similarity_encoding = encoding.get_similarity_encoding(request.fen_encoding)
        chess_positions_pb = self.search_engine_ctrl.get_chess_positions_pb(
            similarity_encoding=similarity_encoding
        )
        response = backend_service_pb2.GetChessPositionsResponse(positions=chess_positions_pb)

        return response

    def GetChessGame(
        self, request: backend_service_pb2.GetChessGameRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessGameResponse:
        chess_game_pb = self.search_engine_ctrl.get_chess_game_pb(request.game_id)
        response = backend_service_pb2.GetChessGameResponse(game=chess_game_pb)

        return response

    def GetChessGames(
        self, request: backend_service_pb2.GetChessGamesRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessGamesResponse:
        chess_utils.check_fen_encoding_is_valid(request.fen_encoding)

        chess_games_pb = self.search_engine_ctrl.get_chess_games_pb(
            fen_encoding=request.fen_encoding
        )
        response = backend_service_pb2.GetChessGamesResponse(games=chess_games_pb)

        return response

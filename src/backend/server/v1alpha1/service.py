import os
import sys
import traceback

import grpc
import structlog
from chesse.v1alpha1 import backend_service_pb2, services_pb2_grpc
from google.protobuf import json_format

import encoding
from backend.search_engine import factory
from backend.tracing import trace, tracer
from backend.utils import exception, meta, typing, validation

logger = structlog.get_logger()


class BackendService(services_pb2_grpc.BackendServiceServicer, metaclass=meta.Singleton):
    def __init__(self) -> None:
        try:
            self.search_engine_ctrl = factory.SearchEngineFactory.get_controller()
        except (ValueError, exception.InvalidCredentialsError) as e:
            logger.critical(
                "could not instantiate the search engine controller",
                error_code=os.EX_CONFIG,
                error_type=type(e),
                error_message=str(e),
                error_stack_trace=traceback.format_exc(),
            )
            sys.exit(os.EX_CONFIG)

    def GetChessPosition(
        self, request: backend_service_pb2.GetChessPositionRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessPositionResponse:
        structlog.threadlocal.bind_threadlocal(request_args=json_format.MessageToDict(request))

        with tracer.start_as_current_span("input: validation"):
            validation.validate_fen_encoding(request.fen_encoding)

        chess_position_pb = self.search_engine_ctrl.get_chess_position_pb(request.fen_encoding)
        response = backend_service_pb2.GetChessPositionResponse(position=chess_position_pb)

        trace.get_current_span().add_event(
            "request successful",
            typing.flatten_dict(
                {"response.position": json_format.MessageToDict(chess_position_pb)}
            ),
        )

        return response

    def ListChessPositions(
        self, request: backend_service_pb2.ListChessPositionsRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.ListChessPositionsResponse:
        structlog.threadlocal.bind_threadlocal(request_args=json_format.MessageToDict(request))

        with tracer.start_as_current_span("input: validation"):
            validation.validate_fen_encoding(request.fen_encoding)
            validation.validate_pagination_params(
                page_size=request.page_size, page_token=request.page_token
            )

        similarity_encoding = encoding.get_similarity_encoding(request.fen_encoding)
        trace.get_current_span().add_event(
            "similarity encoding generated", {"similarity_encoding": similarity_encoding}
        )

        (
            chess_positions_pb,
            total_size,
            next_page_token,
        ) = self.search_engine_ctrl.get_chess_positions_pb(
            similarity_encoding=similarity_encoding,
            page_size=request.page_size,
            page_token=request.page_token,
        )
        response = backend_service_pb2.ListChessPositionsResponse(
            positions=chess_positions_pb, total_size=total_size, next_page_token=next_page_token
        )

        trace.get_current_span().add_event(
            "request successful",
            {
                "response.total_size": str(total_size),
                "response.positions": ", ".join(
                    [
                        f"{(position.fen_encoding, position.position_stats.nr_games)}"
                        for position in chess_positions_pb
                    ]
                ),
                "response.next_page_token": next_page_token,
            },
        )

        return response

    def GetChessGame(
        self, request: backend_service_pb2.GetChessGameRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.GetChessGameResponse:
        structlog.threadlocal.bind_threadlocal(request_args=json_format.MessageToDict(request))

        chess_game_pb = self.search_engine_ctrl.get_chess_game_pb(request.game_id)
        response = backend_service_pb2.GetChessGameResponse(game=chess_game_pb)

        trace.get_current_span().add_event(
            "request successful",
            typing.flatten_dict({"response.position": json_format.MessageToDict(chess_game_pb)}),
        )

        return response

    def ListChessGames(
        self, request: backend_service_pb2.ListChessGamesRequest, context: grpc.ServicerContext
    ) -> backend_service_pb2.ListChessGamesResponse:
        structlog.threadlocal.bind_threadlocal(request_args=json_format.MessageToDict(request))

        with tracer.start_as_current_span("input: validation"):
            validation.validate_fen_encoding(request.fen_encoding)
            validation.validate_pagination_params(
                page_size=request.page_size, page_token=request.page_token
            )

        (chess_games_pb, total_size, next_page_token,) = self.search_engine_ctrl.get_chess_games_pb(
            fen_encoding=request.fen_encoding,
            page_size=request.page_size,
            page_token=request.page_token,
        )
        response = backend_service_pb2.ListChessGamesResponse(
            games=chess_games_pb, total_size=total_size, next_page_token=next_page_token
        )

        trace.get_current_span().add_event(
            "request successful",
            {
                "response.total_size": str(total_size),
                "response.games.ids": ", ".join([game.id for game in chess_games_pb]),
                "response.next_page_token": next_page_token,
            },
        )

        return response

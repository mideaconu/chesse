import grpc
from chesse_backend_api.v1alpha1 import chesse_pb2, positions_pb2
from chesse_backend_api.v1alpha1.chesse_pb2_grpc import CheSSEBackendServiceServicer
from loguru import logger

from backend.api import controller


class CheSSEBackendService(CheSSEBackendServiceServicer):
    def __init__(self) -> None:
        self.chesse_backend_controller = controller.CheSSEBackendController()

    def GetSimilarPositions(
        self, request: chesse_pb2.GetSimilarPositionsRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetSimilarPositionsResponse:
        """Retrieves similar chess positions from CheSSE."""
        logger.info(f"GetSimilarPositionsRequest: {request}")

        search_position_results = self.chesse_backend_controller.get_search_position_results(
            fen=request.position.fen
        )

        response = chesse_pb2.GetSimilarPositionsResponse(
            similar_positions=[
                positions_pb2.SimilarPosition(
                    position=positions_pb2.Position(fen=position["fen"]),
                    similarity_score=position["similarity_score"],
                    position_stats=positions_pb2.PositionStats(
                        nr_games=position["stats"]["nr_games"],
                        rating_stats=positions_pb2.PositionRatingStats(
                            min=position["stats"]["rating"]["min"],
                            avg=position["stats"]["rating"]["avg"],
                            max=position["stats"]["rating"]["max"],
                        ),
                        result_stats=positions_pb2.PositionResultStats(
                            white=position["stats"]["results"]["white"],
                            draw=position["stats"]["results"]["draw"],
                            black=position["stats"]["results"]["black"],
                        ),
                    ),
                )
                for position in search_position_results
            ]
        )

        logger.info(f"Get Similar Games Response: {response}")

        return response

import grpc
from chesse_backend_api.v1alpha1 import chesse_pb2, games_pb2, positions_pb2
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

        logger.info(f"Get Similar Positions Response: {response}")

        return response

    def GetGames(
        self, request: chesse_pb2.GetGamesRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetGamesResponse:
        """Retrieves the games that a given position appears in."""
        logger.info(f"GetGamesRequest: {request}")

        games = self.chesse_backend_controller.get_games(fen=request.position.fen)

        games_pb = [
            games_pb2.Game(
                id=id,
                context=games_pb2.GameContext(
                    event=game["context"]["event"],
                    date=game["context"]["date"],
                    site=game["context"]["site"],
                    round=game["context"]["round"],
                ),
                white=games_pb2.White(name=game["white"]["name"], elo=game["white"]["elo"]),
                black=games_pb2.Black(name=game["black"]["name"], elo=game["black"]["elo"]),
                result=game["result"],
                nr_moves=len(game["moves"]),
            )
            for id, game in games["games"].items()
        ]

        response = chesse_pb2.GetGamesResponse(
            games=games_pb,
            stats=positions_pb2.PositionStats(
                nr_games=games["stats"]["nr_games"],
                rating_stats=positions_pb2.PositionRatingStats(
                    min=games["stats"]["rating"]["min"],
                    avg=games["stats"]["rating"]["avg"],
                    max=games["stats"]["rating"]["max"],
                ),
                result_stats=positions_pb2.PositionResultStats(
                    white=games["stats"]["results"]["white"],
                    draw=games["stats"]["results"]["draw"],
                    black=games["stats"]["results"]["black"],
                ),
            ),
        )

        logger.info(f"Get Games Response: {response}")

        return response

    def GetGame(
        self, request: chesse_pb2.GetGameRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetGameResponse:
        """Retrieve a chess game."""
        logger.info(f"GetGameRequest: {request}")

        game = self.chesse_backend_controller.get_game(id=request.game_id)

        game_pb = games_pb2.Game(
            id=game["id"],
            context=games_pb2.GameContext(
                event=game["context"]["event"],
                date=game["context"]["date"],
                site=game["context"]["site"],
                round=game["context"]["round"],
            ),
            white=games_pb2.White(name=game["white"]["name"], elo=game["white"]["elo"]),
            black=games_pb2.Black(name=game["black"]["name"], elo=game["black"]["elo"]),
            result=game["result"],
            nr_moves=len(game["moves"]),
        )

        response = chesse_pb2.GetGameResponse(game=game_pb)

        logger.info(f"GetGameResponse: {response}")

        return response

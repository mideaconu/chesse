from ssl import create_default_context

import chess
import grpc
from duchess_backend_api.v1alpha1 import games_pb2, positions_pb2
from duchess_backend_api.v1alpha1.duchess_pb2_grpc import DuchessBackendServiceServicer
from elasticsearch import Elasticsearch

from encoding.activity_encoding import encode as encode_activity
from encoding.connectivity_encoding import encode as encode_connectivity
from encoding.naive_encoding import encode as encode_naively
from utils import logger

LOGGER = logger.get_logger(__name__)


class DuchessBackendService(DuchessBackendServiceServicer):
    def GetSimilarGames(
        self, request: games_pb2.GetSimilarGamesRequest, context: grpc.ServicerContext
    ) -> games_pb2.GetSimilarGamesResponse:
        """Retrieves similar chess games from DUChess."""
        LOGGER.info("Retrieving games similar to position %s...", request.position_fen)
        LOGGER.info("Get Similar Games Request: %s", request)

        position_fen = request.position_fen

        board = chess.Board(fen=position_fen)

        position_encoding = "\n".join(
            [
                "\n".join(encode_naively(board)),
                "\n".join(encode_activity(board)),
                "\n".join(encode_connectivity(board, "attack")),
                "\n".join(encode_connectivity(board, "defense")),
                "\n".join(encode_connectivity(board, "ray-attack")),
            ]
        )

        context = create_default_context(cafile="/Users/mihaideaconu/Documents/http_ca.crt")
        es = Elasticsearch(
            hosts=["https://localhost:9200"],
            http_auth=("elastic", "lCUjVzlIk52a++cG6UCX"),
            ssl_context=context,
        )

        query = {"query": {"match": {"position.encoding": position_encoding}}}

        res = es.search(index="positions", body=query)

        response = games_pb2.GetSimilarGamesResponse(
            games=[
                games_pb2.Game(
                    id=game["id"],
                    position=positions_pb2.Position(fen=result["_source"]["position"]["fen"]),
                )
                for result in res["hits"]["hits"]
                for game in result["_source"]["games"]
            ]
        )

        LOGGER.info("Get Similar Games Response: %s", response)

        return response

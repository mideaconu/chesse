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


class DuchessBackendServiceGRPC(DuchessBackendServiceServicer):
    def GetSimilarGames(
        self, request: games_pb2.GetSimilarGamesRequest, context: grpc.ServicerContext
    ) -> games_pb2.GetSimilarGamesResponse:
        """Retrieves similar chess games from DUCHESS."""
        LOGGER.info("Retrieving games similar to position %s...", request.position_fen)
        LOGGER.debug("Get Similar Games Request: %s", request)

        position_fen = request.position_fen

        board = chess.Board(fen=position_fen)

        position_encoding = "\n".join(
            [
                " ".join(encode_naively(board)),
                " ".join(encode_activity(board)),
                " ".join(encode_connectivity(board, "attack")),
                " ".join(encode_connectivity(board, "defense")),
                " ".join(encode_connectivity(board, "ray-attack")),
            ]
        )

        LOGGER.info(position_encoding)

        context = create_default_context(cafile="/Users/mihaideaconu/Documents/http_ca.crt")
        es = Elasticsearch(
            hosts=["https://localhost:9200"],
            http_auth=("elastic", "q0JTP*8g*KdWcCXekYwM"),
            ssl_context=context,
        )

        query = {"query": {"match": {"position.encoding": position_encoding}}}

        res = es.search(index="positions", body=query)
        print("Got %d Hits:" % res["hits"]["total"]["value"])
        print(res)

        # response = games_pb2.GetSimilarGamesResponse(
        #     games=[
        #         games_pb2.Game(id=, position=positions_pb2.Position(fen=position["fen"])) for position in res["hits"]["hits"]["_source"]
        #     ]
        # )

from ssl import create_default_context

import chess
import grpc
from chesse_backend_api.v1alpha1 import chesse_pb2, games_pb2, positions_pb2
from chesse_backend_api.v1alpha1.chesse_pb2_grpc import CheSSEBackendServiceServicer
from elasticsearch import Elasticsearch

from encoding.activity_encoding import encode as encode_activity
from encoding.connectivity_encoding import encode as encode_connectivity
from encoding.naive_encoding import encode as encode_naively
from utils import logger, query

LOGGER = logger.get_logger(__name__)


class CheSSEBackendService(CheSSEBackendServiceServicer):
    def GetSimilarPositions(
        self, request: chesse_pb2.GetSimilarPositionsRequest, context: grpc.ServicerContext
    ) -> chesse_pb2.GetSimilarPositionsResponse:
        """Retrieves similar chess positions from CheSSE."""
        LOGGER.info("Retrieving positions similar to %s...", request.position.fen)
        LOGGER.info("Get Similar Positions Request: %s", request)

        position_fen = request.position.fen

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
            http_auth=("elastic", "QqLpzhLkR+Rm=b_dSaK9"),
            ssl_context=context,
        )

        positions_query = {"query": {"match": {"position.encoding": position_encoding}}}

        res_pos = es.search(index="positions", body=positions_query)

        fens = [position["_id"] for position in res_pos["hits"]["hits"]]
        games_query = query.get_games_query(fens)
        games_aggs = query.get_games_aggregation(fens)

        final_games_query = {"query": games_query["query"], "aggs": games_aggs["aggs"]}

        print(final_games_query)

        res_gm = es.search(index="games", body=final_games_query)
        # print([game["_id"] for game in res["hits"]["hits"]])

        similar_positions = {}
        for position in res_pos["hits"]["hits"]:
            similar_positions[position["_id"]] = {"score": position["_score"]}

        for position in res_gm["aggregations"]["by_fen"]["fen"]["buckets"]:
            fen = position["key"].split(" ")[0]
            similar_positions[fen]["nr_games"] = position["doc_count"]
            similar_positions[fen]["rating_stats"] = {
                "min": int(
                    min(
                        position["white"]["min_elo"]["value"], position["black"]["min_elo"]["value"]
                    )
                ),
                "avg": (
                    position["white"]["avg_elo"]["value"] + position["black"]["avg_elo"]["value"]
                )
                / 2,
                "max": int(
                    max(
                        position["white"]["max_elo"]["value"], position["black"]["max_elo"]["value"]
                    )
                ),
            }

            similar_positions[fen]["result_stats"] = {
                "white_win_pct": 0,
                "draw_pct": 0,
                "black_win_pct": 0,
            }
            for side in position["results"]["white_won"]["buckets"]:
                if side["key"] == 1:
                    similar_positions[fen]["result_stats"]["white_win_pct"] = round(
                        side["doc_count"] / similar_positions[fen]["nr_games"] * 100, 2
                    )
                elif side["key"] == 0.5:
                    similar_positions[fen]["result_stats"]["draw_pct"] = round(
                        side["doc_count"] / similar_positions[fen]["nr_games"] * 100, 2
                    )
                elif side["key"] == 0:
                    similar_positions[fen]["result_stats"]["black_win_pct"] = round(
                        side["doc_count"] / similar_positions[fen]["nr_games"] * 100, 2
                    )

        print(similar_positions)

        response = chesse_pb2.GetSimilarPositionsResponse(
            similar_positions=[
                positions_pb2.SimilarPosition(
                    position=positions_pb2.Position(fen=p_key),
                    similarity_score=p_value["score"],
                    position_stats=positions_pb2.PositionStats(
                        nr_games=p_value["nr_games"],
                        rating_stats=positions_pb2.PositionRatingStats(
                            min=p_value["rating_stats"]["min"],
                            avg=p_value["rating_stats"]["avg"],
                            max=p_value["rating_stats"]["max"],
                        ),
                        result_stats=positions_pb2.PositionResultStats(
                            white_win_pct=p_value["result_stats"]["white_win_pct"],
                            draw_pct=p_value["result_stats"]["draw_pct"],
                            black_win_pct=p_value["result_stats"]["black_win_pct"],
                        ),
                    ),
                )
                for p_key, p_value in similar_positions.items()
            ]
        )

        LOGGER.info("Get Similar Games Response: %s", response)

        return response

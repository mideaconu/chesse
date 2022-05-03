import os
import ssl
import warnings
from typing import Iterable

import elasticsearch as es
import elasticsearch_dsl as es_dsl
from elasticsearch.exceptions import ElasticsearchWarning
from loguru import logger

from backend.search_engine import controller_interface
from utils.typing import JSON

warnings.simplefilter("ignore", ElasticsearchWarning)


def _filter_similar_positions(similar_positions_raw: JSON) -> JSON:
    """Filters the raw ES response so that only relevant information in the
    similar positions response is kept."""
    similar_positions = [
        {"fen": position["_source"]["position"]["fen"], "similarity_score": position["_score"]}
        for position in similar_positions_raw
    ]
    return similar_positions


def _filter_position_stats(position_stats_raw: JSON) -> JSON:
    """Filters the raw ES response so that only relevant information in the
    positions stats response is kept."""
    positions_stats = {}
    for bucket in position_stats_raw["aggregations"]["category_fen"]["fen"]["buckets"]:
        fen = bucket["key"].partition(" ")[0]
        positions_stats[fen] = {
            "nr_games": bucket["doc_count"],
            "rating": {
                "min": int(
                    min(bucket["white"]["min_elo"]["value"], bucket["black"]["min_elo"]["value"])
                ),
                "avg": int(
                    (bucket["white"]["avg_elo"]["value"] + bucket["black"]["avg_elo"]["value"]) / 2
                ),
                "max": int(
                    max(bucket["white"]["max_elo"]["value"], bucket["black"]["max_elo"]["value"])
                ),
            },
            "results": {
                "white": 0,
                "draw": 0,
                "black": 0,
            },
        }
        for side in bucket["results"]["side_won"]["buckets"]:
            match side["key"]:
                case 1:
                    positions_stats[fen]["results"]["white"] = (
                        side["doc_count"] / positions_stats[fen]["nr_games"] * 100
                    )
                case 0.5:
                    positions_stats[fen]["results"]["draw"] = (
                        side["doc_count"] / positions_stats[fen]["nr_games"] * 100
                    )
                case 0:
                    positions_stats[fen]["results"]["black"] = (
                        side["doc_count"] / positions_stats[fen]["nr_games"] * 100
                    )
                case _:
                    logger.error(
                        f"Error processing positions stats: illegal winning side: {side['key']}"
                    )

    return positions_stats


def _filter_games(games_raw: JSON) -> JSON:
    """Filters the raw ES response so that only relevant information in the
    games response is kept."""
    games = {"games": {}, "stats": {}}
    for game in games_raw["hits"]["hits"]:
        games["games"][game["_id"]] = {
            "context": {
                "event": game["_source"]["context"]["event"],
                "date": game["_source"]["context"]["date"],
                "site": game["_source"]["context"]["site"],
                "round": game["_source"]["context"]["round"],
            },
            "white": {
                "name": game["_source"]["white"]["name"],
                "elo": game["_source"]["white"]["elo"],
            },
            "black": {
                "name": game["_source"]["black"]["name"],
                "elo": game["_source"]["black"]["elo"],
            },
            "result": game["_source"]["result"],
            "moves": game["_source"]["moves"],
        }
    print(games_raw["aggregations"])
    games["stats"] = {
        "nr_games": games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["doc_count"],
        "rating": {
            "min": int(
                min(
                    games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["white"][
                        "min_elo"
                    ]["value"],
                    games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["black"][
                        "min_elo"
                    ]["value"],
                )
            ),
            "avg": int(
                (
                    games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["white"][
                        "avg_elo"
                    ]["value"]
                    + games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["black"][
                        "avg_elo"
                    ]["value"]
                )
                / 2
            ),
            "max": int(
                max(
                    games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["white"][
                        "max_elo"
                    ]["value"],
                    games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["black"][
                        "max_elo"
                    ]["value"],
                )
            ),
        },
        "results": {
            "white": 0,
            "draw": 0,
            "black": 0,
        },
    }
    for side in games_raw["aggregations"]["category_fen"]["fen"]["buckets"][0]["results"][
        "side_won"
    ]["buckets"]:
        match side["key"]:
            case 1:
                games["stats"]["results"]["white"] = (
                    side["doc_count"] / games["stats"]["nr_games"] * 100
                )
            case 0.5:
                games["stats"]["results"]["draw"] = (
                    side["doc_count"] / games["stats"]["nr_games"] * 100
                )
            case 0:
                games["stats"]["results"]["black"] = (
                    side["doc_count"] / games["stats"]["nr_games"] * 100
                )
            case _:
                logger.error(
                    f"Error processing positions stats: illegal winning side: {side['key']}"
                )

    return games


class ESController(controller_interface.AbstractSearchEngineController):
    def __init__(self) -> None:
        url = os.getenv("SEARCH_ENGINE_URL")
        username = os.getenv("SEARCH_ENGINE_USERNAME")
        password = os.getenv("SEARCH_ENGINE_PASSWORD")

        context = ssl.create_default_context(cafile="/Users/mihaideaconu/Documents/http_ca.crt")
        self.client = es.Elasticsearch(url, http_auth=(username, password), ssl_context=context)

        logger.info(f"Initialised Search Engine Controller at {url}.")

    def get_similar_positions(self, position_encoding: str) -> JSON:
        # Querying similar positions using the position encoding
        query = es_dsl.Search(using=self.client, index="positions").query(
            "match", position__encoding=position_encoding
        )
        response = query.execute()

        similar_positions_raw = response.to_dict()["hits"]["hits"]
        similar_positions = _filter_similar_positions(similar_positions_raw)

        return similar_positions

    def get_positions_stats(self, fen_list: Iterable[str]) -> JSON:
        # Each move in the games has an associated FEN encoding of the position
        # resulting after the move is made. However, these FEN encodings have
        # additional information about the state of the game, as opposed to the
        # position FENs generated ad-hoc (e.g. castling or en-passant rights).
        # See https://www.chess.com/terms/fen-chess for more details. Because
        # of that, we query the move FEN encodings that start with the given
        # position FEN encodings.
        fen_list_regex = "|".join([f"({fen}.*)" for fen in fen_list])

        query = es_dsl.Search(using=self.client, index="games").query(
            "nested",
            path="moves",
            query=es_dsl.Q("bool", should=[{"prefix": {"moves.fen": fen}} for fen in fen_list]),
        )
        query.aggs.bucket("category_fen", "nested", path="moves").bucket(
            "fen", "terms", field="moves.fen", include=fen_list_regex
        )
        query.aggs["category_fen"]["fen"].bucket("white", "reverse_nested").metric(
            "min_elo", "min", field="white.elo"
        ).metric("max_elo", "max", field="white.elo").metric("avg_elo", "avg", field="white.elo")
        query.aggs["category_fen"]["fen"].bucket("black", "reverse_nested").metric(
            "min_elo", "min", field="black.elo"
        ).metric("max_elo", "max", field="black.elo").metric("avg_elo", "avg", field="black.elo")
        query.aggs["category_fen"]["fen"].bucket("results", "reverse_nested").metric(
            "side_won", "terms", field="result"
        )

        response = query.execute()
        positions_stats_raw = response.to_dict()
        positions_stats = _filter_position_stats(positions_stats_raw)

        logger.debug(positions_stats)

        return positions_stats

    def get_games(self, fen: str) -> JSON:
        fen_regex = f"{fen}.*"

        query = es_dsl.Search(using=self.client, index="games").query(
            "nested", path="moves", query=es_dsl.Q("regexp", moves__fen=fen_regex)
        )
        query.aggs.bucket("category_fen", "nested", path="moves").bucket(
            "fen", "terms", field="moves.fen", include=fen_regex
        )
        query.aggs["category_fen"]["fen"].bucket("white", "reverse_nested").metric(
            "min_elo", "min", field="white.elo"
        ).metric("max_elo", "max", field="white.elo").metric("avg_elo", "avg", field="white.elo")
        query.aggs["category_fen"]["fen"].bucket("black", "reverse_nested").metric(
            "min_elo", "min", field="black.elo"
        ).metric("max_elo", "max", field="black.elo").metric("avg_elo", "avg", field="black.elo")
        query.aggs["category_fen"]["fen"].bucket("results", "reverse_nested").metric(
            "side_won", "terms", field="result"
        )

        response = query.execute()
        games_raw = response.to_dict()
        games = _filter_games(games_raw)

        logger.debug(games)

        return games

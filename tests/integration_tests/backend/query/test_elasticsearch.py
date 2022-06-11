import ssl

import elasticsearch as es
import pytest

from backend.search_engine.query import elasticsearch as es_query
from tests import data as test_data


@pytest.fixture(scope="module")
def elasticsearch():
    ssl_context = ssl.create_default_context(cafile="config/ca.crt")
    yield es.Elasticsearch(
        "https://localhost:9201", http_auth=("elastic", "elastic"), ssl_context=ssl_context
    )


def test_get_chess_position_query(elasticsearch):
    # GIVEN
    query = es_query.get_chess_position_query(test_data.chess_position_json["fen_encoding"])

    # THEN
    assert elasticsearch.indices.validate_query(index="games", query=query)["valid"]


def test_get_similar_positions_query(elasticsearch):
    # GIVEN
    query = es_query.get_similar_positions_query(
        test_data.chess_position_json["similarity_encoding"]
    )

    # THEN
    assert elasticsearch.indices.validate_query(index="positions", query=query)["valid"]


def test_get_chess_game_query(elasticsearch):
    # GIVEN
    query = es_query.get_chess_game_query(test_data.chess_game_json["id"])

    # THEN
    assert elasticsearch.indices.validate_query(index="games", query=query)["valid"]


def test_get_get_chess_games_query(elasticsearch):
    # GIVEN
    query = es_query.get_chess_games_query(test_data.chess_position_json["fen_encoding"])

    # THEN
    assert elasticsearch.indices.validate_query(index="games", query=query)["valid"]
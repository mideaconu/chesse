import os
from unittest import mock

import pytest

from backend.search_engine.controller import elasticsearch
from backend.utils import exception
from tests import data as test_data

MockElasticsearch: mock.Mock

failed_query = {"_shards": {"total": 1, "successful": 0, "unsuccessful": 1}}


@pytest.fixture(scope="class")
def elasticsearch_controller():
    with mock.patch(
        "backend.search_engine.controller.elasticsearch.es.Elasticsearch"
    ) as mock_elasticsearch, mock.patch.dict(
        os.environ,
        {
            "ELASTICSEARCH_USERNAME": "username",
            "ELASTICSEARCH_PASSWORD": "password",
            "ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES": "tests/data/backend/elasticsearch/fake.crt",
        },
        clear=True,
    ):
        global MockElasticsearch

        MockElasticsearch = mock.Mock()
        mock_elasticsearch.return_value = MockElasticsearch

        yield elasticsearch.ElasticsearchController()


class TestElasticsearchController:
    def test_get_chess_position_pb(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(return_value=test_data.chess_position_response_json)

        # WHEN
        chess_position = elasticsearch_controller.get_chess_position_pb(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_position == test_data.chess_position_pb

    def test_get_chess_position_pb_query_unsuccessful(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(return_value=failed_query)

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_position_pb(
                fen_encoding=test_data.chess_position_json["fen_encoding"]
            )

    def test_get_chess_positions_pb_by_similarity_encoding(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(
            side_effect=[
                test_data.similar_positions_response_json,
                test_data.positions_stats_response_json,
            ]
        )

        # WHEN
        chess_positions = elasticsearch_controller.get_chess_positions_pb(
            similarity_encoding=test_data.chess_position_json["similarity_encoding"]
        )

        # THEN
        assert chess_positions == test_data.chess_positions_pb

    @pytest.mark.parametrize(
        "responses",
        [
            pytest.param(
                [failed_query, test_data.positions_stats_response_json],
                id="Failed similar positions query",
            ),
            pytest.param(
                [test_data.similar_positions_response_json, failed_query],
                id="Failed positions stats query",
            ),
        ],
    )
    def test_get_chess_positions_pb_by_similarity_encoding_query_unsuccessful(
        self, elasticsearch_controller, responses
    ):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(side_effect=responses)

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_positions_pb(
                similarity_encoding=test_data.chess_position_json["similarity_encoding"]
            )

    def test_get_chess_game_pb(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(side_effect=[test_data.chess_game_response_json])

        # WHEN
        chess_game = elasticsearch_controller.get_chess_game_pb(test_data.chess_game_json["id"])

        # THEN
        assert chess_game == test_data.chess_game_pb

    def test_get_chess_game_pb_query_unsuccessful(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(return_value=failed_query)

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_game_pb(test_data.chess_game_json["id"])

    def test_get_chess_games_pb_by_fen_encoding(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(return_value=test_data.chess_games_response_json)

        # WHEN
        chess_games = elasticsearch_controller.get_chess_games_pb(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_games == test_data.chess_games_pb

    def test_get_chess_games_pb_by_fen_encoding_query_unsuccessful(self, elasticsearch_controller):
        # GIVEN
        global MockElasticsearch
        MockElasticsearch.search = mock.Mock(return_value=failed_query)

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_games_pb(
                fen_encoding=test_data.chess_position_json["fen_encoding"]
            )

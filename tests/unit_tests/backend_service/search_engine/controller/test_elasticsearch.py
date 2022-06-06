import os
from unittest import mock

import pytest
from elasticsearch_dsl import Search
from elasticsearch_dsl.response import Response

from backend_service.search_engine.controller import elasticsearch
from backend_service.utils import exception
from tests import data as test_data

MockElasticsearch: mock.Mock()


@pytest.fixture(scope="function")
def elasticsearch_controller():
    with mock.patch(
        "backend_service.search_engine.controller.elasticsearch.es.Elasticsearch"
    ) as mock_elasticsearch, mock.patch.dict(
        os.environ,
        {
            "SEARCH_ENGINE_USERNAME": "username",
            "SEARCH_ENGINE_PASSWORD": "password",
            "SEARCH_ENGINE_CERT_PATH": "tests/data/backend_service/elasticsearch/fake.crt",
        },
        clear=True,
    ):
        global MockElasticsearch

        MockElasticsearch = mock.Mock()
        mock_elasticsearch.return_value = MockElasticsearch

        yield elasticsearch.ElasticsearchController()


class TestElasticsearchController:
    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_position_pb(self, mock_es_dsl, elasticsearch_controller):
        # GIVEN
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=test_data.chess_position_response_json
        )

        # WHEN
        chess_position = elasticsearch_controller.get_chess_position_pb(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_position == test_data.chess_position_pb

    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_position_pb_query_unsuccessful(self, mock_es_dsl, elasticsearch_controller):
        # GIVEN
        response = test_data.chess_position_response_json
        response["_shards"]["successful"] = 0
        response["_shards"]["failed"] = 1
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=response
        )

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_position_pb(
                fen_encoding=test_data.chess_position_json["fen_encoding"]
            )

    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_positions_pb_by_similarity_encoding(
        self, mock_es_dsl, elasticsearch_controller
    ):
        # GIVEN
        mock_es_dsl.Search.return_value.query.return_value.execute.side_effect = (
            Response(search=Search(), response=test_data.similar_positions_response_json),
            Response(search=Search(), response=test_data.positions_stats_response_json),
        )

        # WHEN
        chess_positions = elasticsearch_controller.get_chess_positions_pb(
            similarity_encoding=test_data.chess_position_json["similarity_encoding"]
        )

        # THEN
        assert chess_positions == test_data.chess_positions_pb

    @pytest.mark.parametrize(
        "response",
        [
            pytest.param(
                test_data.similar_positions_response_json, id="Similar positions response"
            ),
            pytest.param(test_data.positions_stats_response_json, id="Positions stats response"),
        ],
    )
    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_positions_pb_by_similarity_encoding_query_unsuccessful(
        self, mock_es_dsl, elasticsearch_controller, response
    ):
        # GIVEN
        response["_shards"]["successful"] = 0
        response["_shards"]["failed"] = 1
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=response
        )

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_positions_pb(
                similarity_encoding=test_data.chess_position_json["similarity_encoding"]
            )

    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_game_pb(self, mock_es_dsl, elasticsearch_controller):
        # GIVEN
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=test_data.chess_game_response_json
        )

        # WHEN
        chess_game = elasticsearch_controller.get_chess_game_pb(test_data.chess_game_json["id"])

        # THEN
        assert chess_game == test_data.chess_game_pb

    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_game_pb_query_unsuccessful(self, mock_es_dsl, elasticsearch_controller):
        # GIVEN
        response = test_data.chess_game_response_json
        response["_shards"]["successful"] = 0
        response["_shards"]["failed"] = 1
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=response
        )

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_game_pb(test_data.chess_game_json["id"])

    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_games_pb_by_fen_encoding(self, mock_es_dsl, elasticsearch_controller):
        # GIVEN
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=test_data.chess_games_response_json
        )

        # WHEN
        chess_games = elasticsearch_controller.get_chess_games_pb(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_games == test_data.chess_games_pb

    @mock.patch("backend_service.search_engine.controller.elasticsearch.es_dsl")
    def test_get_chess_games_pb_by_fen_encoding_query_unsuccessful(
        self, mock_es_dsl, elasticsearch_controller
    ):
        # GIVEN
        response = test_data.chess_games_response_json
        response["_shards"]["successful"] = 0
        response["_shards"]["failed"] = 1
        mock_es_dsl.Search.return_value.query.return_value.execute.return_value = Response(
            search=Search(), response=response
        )

        # THEN
        with pytest.raises(exception.SearchEngineQueryError):
            elasticsearch_controller.get_chess_games_pb(
                fen_encoding=test_data.chess_position_json["fen_encoding"]
            )

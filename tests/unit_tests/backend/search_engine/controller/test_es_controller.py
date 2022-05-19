import os
import random
from unittest import mock

import pytest

from backend.search_engine import controller as controller
from tests import data as test_data

MockElasticsearch: mock.Mock()


@pytest.fixture(scope="function")
def es_controller():
    with mock.patch(
        "backend.search_engine.controller.es_controller.es.Elasticsearch"
    ) as mock_elasticsearch, mock.patch.dict(
        os.environ,
        {"SEARCH_ENGINE_USERNAME": "username", "SEARCH_ENGINE_PASSWORD": "password"},
        clear=True,
    ):
        global MockElasticsearch

        MockElasticsearch = mock.Mock()
        mock_elasticsearch.return_value = MockElasticsearch

        yield controller.ESController()


class TestESController:
    @mock.patch("backend.search_engine.controller.es_controller.es_dsl")
    @mock.patch("backend.search_engine.controller.es_controller.es_utils")
    def test_get_chess_position_by_fen_encoding(self, mock_es_utils, mock_es_dsl, es_controller):
        # GIVEN
        filtered_chess_position = {
            "fen_encoding": test_data.chess_position_json["fen_encoding"],
            "similarity_encoding": test_data.chess_position_json["similarity_encoding"],
        }
        mock_es_utils.filter_chess_position_response.return_value = filtered_chess_position

        MockResponse = mock.Mock()
        MockResponse.success.return_value = True
        MockResponse.hits.return_value = {"hits": [test_data.chess_position_json]}
        mock_es_dsl.Search.query.execute.return_value = MockResponse

        # WHEN
        chess_position = es_controller.get_chess_position(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_position == filtered_chess_position

    @mock.patch("backend.search_engine.controller.es_controller.es_dsl")
    @mock.patch("backend.search_engine.controller.es_controller.es_utils")
    def test_get_chess_position_stats_by_fen_encoding(
        self, mock_es_utils, mock_es_dsl, es_controller
    ):
        # GIVEN
        filtered_chess_position_stats = test_data.chess_position_json["stats"]
        mock_es_utils.filter_chess_position_stats_response.return_value = (
            filtered_chess_position_stats
        )

        MockResponse = mock.Mock()
        MockResponse.success.return_value = True
        mock_es_dsl.Search.query.execute.return_value = MockResponse

        # WHEN
        chess_position_stats = es_controller.get_chess_position_stats(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_position_stats == filtered_chess_position_stats

    @mock.patch("backend.search_engine.controller.es_controller.es_dsl")
    @mock.patch("backend.search_engine.controller.es_controller.es_utils")
    def test_get_chess_positions_by_similarity_encoding(
        self, mock_es_utils, mock_es_dsl, es_controller
    ):
        # GIVEN
        filtered_chess_positions = [
            {
                "fen_encoding": chess_position["fen_encoding"],
                "similarity_encoding": chess_position["similarity_encoding"],
                "similarity_score": random.random(),
            }
            for chess_position in test_data.chess_positions_json
        ]
        mock_es_utils.filter_chess_positions_response.return_value = filtered_chess_positions

        MockResponse = mock.Mock()
        MockResponse.success.return_value = True
        mock_es_dsl.Search.query.execute.return_value = MockResponse

        # WHEN
        chess_positions = es_controller.get_chess_positions(
            similarity_encoding=test_data.chess_position_json["similarity_encoding"]
        )

        # THEN
        assert chess_positions == filtered_chess_positions

    @mock.patch("backend.search_engine.controller.es_controller.es_dsl")
    @mock.patch("backend.search_engine.controller.es_controller.es_utils")
    def test_get_chess_positions_stats_by_fen_encoding(
        self, mock_es_utils, mock_es_dsl, es_controller
    ):
        # GIVEN
        filtered_chess_positions_stats = [
            chess_position["stats"] for chess_position in test_data.chess_positions_json
        ]
        mock_es_utils.filter_chess_positions_stats_response.return_value = (
            filtered_chess_positions_stats
        )

        MockResponse = mock.Mock()
        MockResponse.success.return_value = True
        mock_es_dsl.Search.query.execute.return_value = MockResponse

        # WHEN
        chess_positions_stats = es_controller.get_chess_positions_stats(
            fen_encodings=[
                chess_position["fen_encoding"] for chess_position in test_data.chess_positions_json
            ]
        )

        # THEN
        assert chess_positions_stats == filtered_chess_positions_stats

    @mock.patch("backend.search_engine.controller.es_controller.es_dsl")
    @mock.patch("backend.search_engine.controller.es_controller.es_utils")
    def test_get_chess_game_by_id(self, mock_es_utils, mock_es_dsl, es_controller):
        # GIVEN
        filtered_chess_game = test_data.chess_game_json
        mock_es_utils.filter_chess_game_response.return_value = filtered_chess_game

        MockResponse = mock.Mock()
        MockResponse.success.return_value = True
        mock_es_dsl.Search.query.execute.return_value = MockResponse

        # WHEN
        chess_game = es_controller.get_chess_game(id=test_data.chess_game_json["id"])

        # THEN
        assert chess_game == filtered_chess_game

    @mock.patch("backend.search_engine.controller.es_controller.es_dsl")
    @mock.patch("backend.search_engine.controller.es_controller.es_utils")
    def test_get_chess_games_by_fen_encoding(self, mock_es_utils, mock_es_dsl, es_controller):
        # GIVEN
        filtered_chess_games = test_data.chess_games_json
        mock_es_utils.filter_chess_games_response.return_value = filtered_chess_games

        MockResponse = mock.Mock()
        MockResponse.success.return_value = True
        mock_es_dsl.Search.query.execute.return_value = MockResponse

        # WHEN
        chess_games = es_controller.get_chess_games(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_games == filtered_chess_games

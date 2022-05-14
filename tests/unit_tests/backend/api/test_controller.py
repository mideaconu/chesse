from unittest import mock

import pytest

from backend.api.controller import CheSSEBackendController
from tests import data as test_data

MockESController: mock.Mock = None


@pytest.fixture(scope="function")
def chess_backend_controller():
    global MockESController

    MockESController = mock.Mock()

    with mock.patch(
        "backend.api.controller.factory.CheSSEBackendFactory"
    ) as mock_chesse_backend_factory:
        MockESController.get_chess_position.return_value = {
            k: v
            for k, v in test_data.chess_position_json.items()
            if k in ["fen_encoding", "similarity_encoding"]
        }
        MockESController.get_chess_position_stats.return_value = test_data.chess_position_json[
            "stats"
        ]

        MockESController.get_chess_positions.return_value = [
            {k: v for k, v in position.items() if k in ["fen_encoding", "similarity_encoding"]}
            for position in test_data.chess_positions_json
        ]
        MockESController.get_chess_positions_stats.return_value = {
            position["fen_encoding"]: position["stats"]
            for position in test_data.chess_positions_json
        }

        MockESController.get_chess_game.return_value = test_data.chess_game_json

        MockESController.get_chess_games.return_value = test_data.chess_games_json

        mock_chesse_backend_factory.get_search_engine_controller.return_value = MockESController

        yield CheSSEBackendController()


class TestCheSSEBackendService:
    @mock.patch("backend.api.controller.encoding_utils.check_fen_encoding_is_valid")
    def test_get_chess_position(self, mock_check_fen_encoding_is_valid, chess_backend_controller):
        # WHEN
        chess_position = chess_backend_controller.get_chess_position(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_position == test_data.chess_position_json

    @mock.patch("backend.api.controller.encoding.get_similarity_encoding")
    @mock.patch("backend.api.controller.encoding_utils.check_fen_encoding_is_valid")
    def test_get_chess_positions(
        self,
        mock_check_fen_encoding_is_valid,
        mock_get_similarity_encoding,
        chess_backend_controller,
    ):
        # GIVEN
        mock_get_similarity_encoding.return_value = test_data.chess_position_json[
            "similarity_encoding"
        ]

        # WHEN
        chess_positions = chess_backend_controller.get_chess_positions(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_positions == test_data.chess_positions_json

    def test_get_chess_game(self, chess_backend_controller):
        # WHEN
        chess_game = chess_backend_controller.get_chess_game(id=test_data.chess_game_json["id"])

        # THEN
        assert chess_game == test_data.chess_game_json

    def test_get_chess_games(self, chess_backend_controller):
        # WHEN
        chess_games = chess_backend_controller.get_chess_games(
            fen_encoding=test_data.chess_position_json["fen_encoding"]
        )

        # THEN
        assert chess_games == test_data.chess_games_json

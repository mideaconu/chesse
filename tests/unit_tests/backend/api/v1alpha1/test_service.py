from unittest import mock

import pytest
from chesse_backend_api.v1alpha1 import chesse_pb2

import grpc
from backend.api import server
from tests import data as test_data

port = 1234
MockCheSSEBackendController: mock.Mock = None


@pytest.fixture(scope="function")
def mock_chesse_backend_server():
    global MockCheSSEBackendController
    MockCheSSEBackendController = mock.Mock()
    with mock.patch(
        "backend.api.v1alpha1.service.controller.CheSSEBackendController"
    ) as mock_chesse_backend_controller:
        mock_chesse_backend_controller.return_value = MockCheSSEBackendController
        chesse_backend_server = server.CheSSEBackendServer(port=port)
    chesse_backend_server.start()
    yield
    chesse_backend_server.stop()


@pytest.fixture(scope="function")
def mock_chesse_backend_client_stub(mock_chesse_backend_server):
    from chesse_backend_api.v1alpha1.chesse_pb2_grpc import CheSSEBackendServiceStub

    channel = grpc.insecure_channel(f"localhost:{port}")
    yield CheSSEBackendServiceStub(channel)
    channel.close()


class TestCheSSEBackendService:
    @mock.patch("backend.api.v1alpha1.service.pb2_utils.convert_json_to_pb2")
    def test_GetChessPosition(
        self, mock_convert_json_to_pb2, mock_chesse_backend_server, mock_chesse_backend_client_stub
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockCheSSEBackendController.get_chess_position.return_value = test_data.chess_position_json
        mock_convert_json_to_pb2.return_value = test_data.chess_position_pb2

        # WHEN
        chess_position = mock_chesse_backend_client_stub.GetChessPosition(
            chesse_pb2.GetChessPositionRequest(fen_encoding=fen_encoding)
        )

        # THEN
        MockCheSSEBackendController.get_chess_position.assert_called_once_with(
            fen_encoding=fen_encoding
        )
        mock_convert_json_to_pb2.assert_called_once_with(
            chess_position_json=test_data.chess_position_json
        )
        assert chess_position.position == test_data.chess_position_pb2

    @mock.patch("backend.api.v1alpha1.service.pb2_utils.convert_json_to_pb2")
    def test_GetChessPositions(
        self, mock_convert_json_to_pb2, mock_chesse_backend_server, mock_chesse_backend_client_stub
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockCheSSEBackendController.get_chess_positions.return_value = (
            test_data.chess_positions_json
        )
        mock_convert_json_to_pb2.return_value = test_data.chess_positions_pb2

        # WHEN
        chess_positions = mock_chesse_backend_client_stub.GetChessPositions(
            chesse_pb2.GetChessPositionsRequest(fen_encoding=fen_encoding)
        )

        # THEN
        MockCheSSEBackendController.get_chess_positions.assert_called_once_with(
            fen_encoding=fen_encoding
        )
        mock_convert_json_to_pb2.assert_called_once_with(
            chess_positions_json=test_data.chess_positions_json
        )
        assert all(
            position in test_data.chess_positions_pb2 for position in chess_positions.positions
        )

    @mock.patch("backend.api.v1alpha1.service.pb2_utils.convert_json_to_pb2")
    def test_GetChessGame(
        self, mock_convert_json_to_pb2, mock_chesse_backend_server, mock_chesse_backend_client_stub
    ):
        # GIVEN
        game_id = "eJwLSixJTVFwKs3JSS1RSE/MTa0xMjA01jMw1jMyqDE0tDIxtTI0qLGvSS9KTc2Oz0usyqzJz6hMTcwAABDeEwI="
        MockCheSSEBackendController.get_chess_game.return_value = test_data.chess_game_json
        mock_convert_json_to_pb2.return_value = test_data.chess_game_pb2

        # WHEN
        chess_game = mock_chesse_backend_client_stub.GetChessGame(
            chesse_pb2.GetChessGameRequest(game_id=game_id)
        )

        # THEN
        MockCheSSEBackendController.get_chess_game.assert_called_once_with(id=game_id)
        mock_convert_json_to_pb2.assert_called_once_with(chess_game_json=test_data.chess_game_json)
        assert chess_game.game == test_data.chess_game_pb2

    @mock.patch("backend.api.v1alpha1.service.pb2_utils.convert_json_to_pb2")
    def test_GetChessGames(
        self, mock_convert_json_to_pb2, mock_chesse_backend_server, mock_chesse_backend_client_stub
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockCheSSEBackendController.get_chess_games.return_value = test_data.chess_games_json
        mock_convert_json_to_pb2.return_value = test_data.chess_games_pb2

        # WHEN
        chess_games = mock_chesse_backend_client_stub.GetChessGames(
            chesse_pb2.GetChessGamesRequest(fen_encoding=fen_encoding)
        )

        # THEN
        MockCheSSEBackendController.get_chess_games.assert_called_once_with(
            fen_encoding=fen_encoding
        )
        mock_convert_json_to_pb2.assert_called_once_with(
            chess_games_json=test_data.chess_games_json
        )
        assert all(game in test_data.chess_games_pb2 for game in chess_games.games)

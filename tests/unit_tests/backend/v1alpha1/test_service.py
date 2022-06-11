from concurrent import futures
from unittest import mock

import grpc
import pytest
from chesse.v1alpha1 import backend_service_pb2, services_pb2_grpc

from backend.server.v1alpha1 import interceptor
from backend.server.v1alpha1 import service as v1a1_service
from backend.utils import exception
from tests import data as test_data

port = 1234
similarity_encoding = (
    "rc1 Pf2 Kg2 Ph2 Pa3 Pe3 Pg3 Pb4 Qe4 qc6 pg6 ph6 pa7 pb7 pf7 Rd8 kg8 Rg8|0.67 Rf8|0.78 "
    "Re8|0.89 Rc8|0.89 Rb8|0.78 Ra8|0.67 Rd7|0.89 Rd6|0.78 Rd5|0.67 Rd4|0.56 Rd3|0.45 Rd2|0.34 "
    "Rd1|0.23 Qe8|0.56 Qe7|0.67 Qg6|0.78 Qe6|0.78 Qc6|0.78 Qf5|0.89 Qe5|0.89 Qd5|0.89 Qh4|0.67 "
    "Qg4|0.78 Qf4|0.89 Qd4|0.89 Qc4|0.78 Qf3|0.89 Qd3|0.89 Qc2|0.78 Qb1|0.67 Kh3|0.89 Kf3|0.89 "
    "Kh1|0.89 Kg1|0.89 Kf1|0.89 Pb5|0.89 Pg4|0.89 Pa4|0.89 Ph3|0.89 Pf3|0.89 Ph4|0.78 Pf4|0.78 "
    "kh8|0.89 kf8|0.89 kh7|0.89 kg7|0.89 qe8|0.78 qc8|0.78 qd7|0.89 qc7|0.89 qf6|0.67 qe6|0.78 "
    "qd6|0.89 qb6|0.89 qa6|0.78 qd5|0.89 qc5|0.89 qb5|0.89 qe4|0.78 qc4|0.78 qa4|0.78 qc3|0.67 "
    "qc2|0.56 rc5|0.56 rc4|0.67 rc3|0.78 rc2|0.89 rh1|0.45 rg1|0.56 rf1|0.67 re1|0.78 rd1|0.89 "
    "rb1|0.89 ra1|0.78 pf6|0.89 pb6|0.89 pa6|0.89 ph5|0.89 pg5|0.89 pf5|0.78 pb5|0.78 pa5|0.78 "
    "Q>qc6 Q>pg6 q>Qe4 R>kg8 r<qc6 P<Pe3 P<Pg3 K<Pf2 K<Ph2 K<Pg3 P<Pg3 P<Pb4 Q<Kg2 Q<Pe3 Q<Pb4 "
    "q<rc1 q<pg6 q<pb7 p<qc6 p<pg6 k<pf7 Q=qc6 Q=pg6 Q=pb7 q=Qe4 q=Kg2 R=kg8"
)

MockElasticsearchController: mock.Mock() = None


@pytest.fixture(scope="session", autouse=True)
def mock_chesse_backend_server():
    with mock.patch(
        "backend.server.v1alpha1.service.factory.SearchEngineFactory.get_controller"
    ) as mock_get_controller:
        global MockElasticsearchController

        MockElasticsearchController = mock.Mock()
        mock_get_controller.return_value = MockElasticsearchController

        backend_server = grpc.server(
            futures.ThreadPoolExecutor(),
            interceptors=[interceptor.ExceptionToStatusInterceptor()],
        )
        services_pb2_grpc.add_BackendServiceServicer_to_server(
            v1a1_service.BackendService(), backend_server
        )
        backend_server.add_insecure_port(f"[::]:{port}")

        backend_server.start()
        yield
        backend_server.stop(grace=None)


class TestCheSSEBackendService:
    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessPosition(self, mock_check_fen_encoding_is_valid):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockElasticsearchController.get_chess_position_pb.return_value = test_data.chess_position_pb

        # WHEN
        chess_position = services_pb2_grpc.BackendService.GetChessPosition(
            backend_service_pb2.GetChessPositionRequest(fen_encoding=fen_encoding),
            f"localhost:{port}",
            insecure=True,
        )

        # THEN
        assert isinstance(chess_position, backend_service_pb2.GetChessPositionResponse)
        assert chess_position.position == test_data.chess_position_pb

    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessPosition_invalid_arg_error(self, mock_check_fen_encoding_is_valid):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        mock_check_fen_encoding_is_valid.side_effect = exception.InvalidFENEncodingError
        MockElasticsearchController.get_chess_position_pb.return_value = test_data.chess_position_pb

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessPosition(
                backend_service_pb2.GetChessPositionRequest(fen_encoding=fen_encoding),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    @pytest.mark.parametrize(
        "error_type",
        [
            pytest.param(exception.SearchEngineQueryError, id="Query error"),
            pytest.param(exception.SearchEnginePbConversionError, id="Pb conversion error"),
        ],
    )
    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessPosition_internal_server_error(
        self, mock_check_fen_encoding_is_valid, error_type
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockElasticsearchController.get_chess_position_pb.side_effect = error_type

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessPosition(
                backend_service_pb2.GetChessPositionRequest(fen_encoding=fen_encoding),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INTERNAL

    @mock.patch("backend.server.v1alpha1.service.encoding.get_similarity_encoding")
    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessPositions(
        self, mock_check_fen_encoding_is_valid, mock_get_similarity_encoding
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockElasticsearchController.get_chess_positions_pb.return_value = (
            test_data.chess_positions_pb
        )
        mock_get_similarity_encoding.return_value = similarity_encoding

        # WHEN
        chess_positions = services_pb2_grpc.BackendService.GetChessPositions(
            backend_service_pb2.GetChessPositionsRequest(fen_encoding=fen_encoding),
            f"localhost:{port}",
            insecure=True,
        )

        # THEN
        assert isinstance(chess_positions, backend_service_pb2.GetChessPositionsResponse)
        assert all(
            position in test_data.chess_positions_pb for position in chess_positions.positions
        )

    @mock.patch("backend.server.v1alpha1.service.encoding.get_similarity_encoding")
    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessPositions_invalid_arg_error(
        self, mock_check_fen_encoding_is_valid, mock_get_similarity_encoding
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        mock_check_fen_encoding_is_valid.side_effect = exception.InvalidFENEncodingError
        mock_get_similarity_encoding.return_value = similarity_encoding
        MockElasticsearchController.get_chess_positions_pb.return_value = (
            test_data.chess_positions_pb
        )

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessPositions(
                backend_service_pb2.GetChessPositionsRequest(fen_encoding=fen_encoding),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    @pytest.mark.parametrize(
        "error_type",
        [
            pytest.param(exception.SearchEngineQueryError, id="Query error"),
            pytest.param(exception.SearchEnginePbConversionError, id="Pb conversion error"),
        ],
    )
    @mock.patch("backend.server.v1alpha1.service.encoding.get_similarity_encoding")
    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessPositions_internal_server_error(
        self, mock_check_fen_encoding_is_valid, mock_get_similarity_encoding, error_type
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        mock_get_similarity_encoding.return_value = similarity_encoding
        MockElasticsearchController.get_chess_positions_pb.side_effect = error_type

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessPositions(
                backend_service_pb2.GetChessPositionsRequest(fen_encoding=fen_encoding),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INTERNAL

    def test_GetChessGame(self):
        # GIVEN
        game_id = "eJwLSixJTVFwKs3JSS1RSE/MTa0xMjA01jMw1jMyqDE0tDIxtTI0qLGvSS9KTc2Oz0usyqzJz6hMTcwAABDeEwI="
        MockElasticsearchController.get_chess_game_pb.return_value = test_data.chess_game_pb

        # WHEN
        chess_game = services_pb2_grpc.BackendService.GetChessGame(
            backend_service_pb2.GetChessGameRequest(game_id=game_id),
            f"localhost:{port}",
            insecure=True,
        )

        # THEN
        assert isinstance(chess_game, backend_service_pb2.GetChessGameResponse)
        assert chess_game.game == test_data.chess_game_pb

    @pytest.mark.parametrize(
        "error_type",
        [
            pytest.param(exception.SearchEngineQueryError, id="Query error"),
            pytest.param(exception.SearchEnginePbConversionError, id="Pb conversion error"),
        ],
    )
    def test_GetChessGame_internal_server_error(self, error_type):
        # GIVEN
        game_id = "eJwLSixJTVFwKs3JSS1RSE/MTa0xMjA01jMw1jMyqDE0tDIxtTI0qLGvSS9KTc2Oz0usyqzJz6hMTcwAABDeEwI="
        MockElasticsearchController.get_chess_game_pb.side_effect = error_type

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessGame(
                backend_service_pb2.GetChessGameRequest(game_id=game_id),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INTERNAL

    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessGames(self, mock_check_fen_encoding_is_valid):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockElasticsearchController.get_chess_games_pb.return_value = test_data.chess_games_pb

        # WHEN
        chess_games = services_pb2_grpc.BackendService.GetChessGames(
            backend_service_pb2.GetChessGamesRequest(fen_encoding=fen_encoding),
            f"localhost:{port}",
            insecure=True,
        )

        # THEN
        assert isinstance(chess_games, backend_service_pb2.GetChessGamesResponse)
        assert all(game in test_data.chess_games_pb for game in chess_games.games)

    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessGames_invalid_arg_error(self, mock_check_fen_encoding_is_valid):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        mock_check_fen_encoding_is_valid.side_effect = exception.InvalidFENEncodingError
        MockElasticsearchController.get_chess_games_pb.return_value = test_data.chess_games_pb

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessGames(
                backend_service_pb2.GetChessGamesRequest(fen_encoding=fen_encoding),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    @pytest.mark.parametrize(
        "error_type",
        [
            pytest.param(exception.SearchEngineQueryError, id="Query error"),
            pytest.param(exception.SearchEnginePbConversionError, id="Pb conversion error"),
        ],
    )
    @mock.patch("backend.server.v1alpha1.service.chess_utils.check_fen_encoding_is_valid")
    def test_GetChessGames_internal_server_error(
        self, mock_check_fen_encoding_is_valid, error_type
    ):
        # GIVEN
        fen_encoding = "3R2k1/pp3p2/2q3pp/8/1P2Q3/P3P1P1/5PKP/2r5"
        MockElasticsearchController.get_chess_games_pb.side_effect = error_type

        # WHEN
        with pytest.raises(Exception) as e:
            services_pb2_grpc.BackendService.GetChessGames(
                backend_service_pb2.GetChessGamesRequest(fen_encoding=fen_encoding),
                f"localhost:{port}",
                insecure=True,
            )

        # THEN
        assert e.value.code() == grpc.StatusCode.INTERNAL

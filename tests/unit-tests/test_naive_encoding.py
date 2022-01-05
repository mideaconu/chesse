import chess
import pytest

from src.encoding import naive_encoding


@pytest.mark.parametrize(
    "board, expected_encoding",
    [
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            {
                "Kc1",
                "Qa3",
                "Re1",
                "Re2",
                "Bf2",
                "Bg2",
                "Nc3",
                "Pa2",
                "Pb2",
                "Pc2",
                "Pd4",
                "Pd5",
                "Pf4",
                "Pg4",
                "Ph3",
                "kg8",
                "qc7",
                "ra8",
                "rb8",
                "bd7",
                "bf6",
                "nb6",
                "pa5",
                "pc4",
                "pd6",
                "pe7",
                "pf7",
                "pg5",
                "ph6",
            },
        ),
    ],
)
def test_get_naive_encoding(board, expected_encoding):
    actual_encoding = naive_encoding.get_naive_encoding(board).split()

    assert len(set(actual_encoding)) == len(actual_encoding)
    assert expected_encoding == set(actual_encoding)

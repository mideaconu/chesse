import chess
import pytest

from src.encoding import naive_encoding


@pytest.mark.parametrize(
    "board, expected_encoding",
    [
        pytest.param(
            chess.Board(),
            {
                "Ra1",
                "Nb1",
                "Bc1",
                "Qd1",
                "Ke1",
                "Bf1",
                "Ng1",
                "Rh1",
                "Pa2",
                "Pb2",
                "Pc2",
                "Pd2",
                "Pe2",
                "Pf2",
                "Pg2",
                "Ph2",
                "pa7",
                "pb7",
                "pc7",
                "pd7",
                "pe7",
                "pf7",
                "pg7",
                "ph7",
                "ra8",
                "nb8",
                "bc8",
                "qd8",
                "ke8",
                "bf8",
                "ng8",
                "rh8",
            },
            id="Initial position",
        )
    ],
)
def test_get_naive_encodings(board, expected_encoding):
    actual_encoding = set(naive_encoding.get_naive_encoding(board).split())
    assert expected_encoding == actual_encoding

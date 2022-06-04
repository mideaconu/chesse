import pytest

from utils.encoding import get_naive_encoding


@pytest.mark.parametrize(
    "fen_encoding, expected_activity_encoding",
    [
        pytest.param(
            "r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1",
            "Ra1 Qd1 Ke1 Bf1 Ng1 Rh1 Pa2 Pb2 Nd2 Pf2 Pg2 Ph2 Pc3 Be3 pe4 bc5 pe6 pa7 pb7 nd7 pf7 "
            "pg7 ph7 ra8 bc8 qd8 ke8 ng8 rh8",
            id="Opening",
        ),
        pytest.param(
            "rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -",
            "Kc1 Re1 Pa2 Pb2 Pc2 Re2 Bf2 Bg2 Qa3 Nc3 Ph3 pc4 Pd4 Pf4 Pg4 pa5 Pd5 pg5 nb6 pd6 bf6 "
            "ph6 qc7 bd7 pe7 pf7 ra8 rb8 kg8",
            id="Middle game",
        ),
        pytest.param(
            "1R1R4/p4pp1/4pk2/2pb1P2/r5Pp/2PK3P/2P5/8 w - - 0 1",
            "Pc2 Pc3 Kd3 Ph3 ra4 Pg4 ph4 pc5 bd5 Pf5 pe6 kf6 pa7 pf7 pg7 Rb8 Rd8",
            id="Endgame",
        ),
    ],
)
def test_get_naive_encoding(fen_encoding, expected_activity_encoding):
    assert get_naive_encoding(fen=fen_encoding) == expected_activity_encoding


@pytest.mark.parametrize(
    "fen_encoding",
    [
        pytest.param("", id="Empty FEN"),
        pytest.param(
            "nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            id="Invalid position: missing square",
        ),
        pytest.param(
            "nbqkbnr/ppppppp/7/7/7/7/PPPPPPP/NBQKBNR w KQkq - 0 1",
            id="Invalid position: missing row",
        ),
        pytest.param(
            "pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", id="Invalid position: missing column"
        ),
        pytest.param(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR X KQkq - 0 1", id="Invalid side to move"
        ),
        pytest.param(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w X - 0 1", id="Invalid castling rights"
        ),
        pytest.param(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq X 0 1",
            id="Invalid en passant rights",
        ),
    ],
)
def test_get_naive_encoding_invalid_fen(fen_encoding):
    with pytest.raises(ValueError):
        get_naive_encoding(fen=fen_encoding)

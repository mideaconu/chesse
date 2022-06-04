import pytest

from utils.encoding import get_activity_encoding


@pytest.mark.parametrize(
    "fen_encoding, expected_activity_encoding",
    [
        pytest.param(
            "r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1",
            "Bh6|0.67 Bg5|0.78 Bc5|0.78 Bf4|0.89 Bd4|0.89 Ne4|0.78 Nc4|0.78 Nf3|0.78 Nb3|0.78 "
            "Nb1|0.78 Nh3|0.78 Nf3|0.78 Ne2|0.78 Ba6|0.45 Bb5|0.56 Bc4|0.67 Bd3|0.78 Be2|0.89 "
            "Ke2|0.89 Qh5|0.56 Qg4|0.67 Qa4|0.67 Qf3|0.78 Qb3|0.78 Qe2|0.89 Qc2|0.89 Qc1|0.89 "
            "Qb1|0.78 Rc1|0.78 Rb1|0.89 Pc4|0.89 Ph3|0.89 Pg3|0.89 Pf3|0.89 Pb3|0.89 Pa3|0.89 "
            "Ph4|0.78 Pg4|0.78 Pf4|0.78 Pb4|0.78 Pa4|0.78 ne7|0.78 nh6|0.78 nf6|0.78 kf8|0.89 "
            "ke7|0.89 qe7|0.89 qc7|0.89 qf6|0.78 qb6|0.78 qg5|0.67 qa5|0.67 qh4|0.56 rb8|0.89 "
            "nf8|0.78 nb8|0.78 nf6|0.78 nb6|0.78 ne5|0.78 bf8|0.67 be7|0.78 bd6|0.89 bb6|0.89 "
            "bd4|0.89 bb4|0.89 be3|0.78 ba3|0.78 ph6|0.89 pg6|0.89 pf6|0.89 pb6|0.89 pa6|0.89 "
            "pe5|0.89 ph5|0.78 pg5|0.78 pf5|0.78 pb5|0.78 pa5|0.78",
            id="Opening",
        ),
        pytest.param(
            "rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -",
            "Nb5|0.78 Ne4|0.78 Na4|0.78 Nd1|0.78 Nb1|0.78 Qd6|0.67 Qc5|0.78 Qa5|0.78 Qb4|0.89 "
            "Qa4|0.89 Qb3|0.89 Be4|0.78 Bf3|0.89 Bh1|0.89 Bf1|0.89 Bh4|0.78 Bg3|0.89 Be3|0.89 "
            "Bg1|0.89 Re7|0.45 Re6|0.56 Re5|0.67 Re4|0.78 Re3|0.89 Rd2|0.89 Rh1|0.67 Rg1|0.78 "
            "Rf1|0.89 Rd1|0.89 Kd2|0.89 Kd1|0.89 Kb1|0.89 Pg5|0.89 Pf5|0.89 Ph4|0.89 Pb3|0.89 "
            "Pb4|0.78 kh8|0.89 kf8|0.89 kh7|0.89 kg7|0.89 rf8|0.56 re8|0.67 rd8|0.78 rc8|0.89 "
            "rb7|0.89 ra7|0.89 ra6|0.78 be8|0.89 bc8|0.89 be6|0.89 bc6|0.89 bf5|0.78 bb5|0.78 "
            "bg4|0.67 ba4|0.67 qd8|0.89 qc8|0.89 qb7|0.89 qa7|0.78 qc6|0.89 qc5|0.78 bh8|0.78 "
            "bg7|0.89 be5|0.89 bd4|0.78 nc8|0.78 nd5|0.78 na4|0.78 pf4|0.89 pe6|0.89 ph5|0.89 "
            "pa4|0.89 pe5|0.78",
            id="Middle game",
        ),
        pytest.param(
            "1R1R4/p4pp1/4pk2/2pb1P2/r5Pp/2PK3P/2P5/8 w - - 0 1",
            "Rh8|0.56 Rg8|0.67 Rf8|0.78 Re8|0.89 Rc8|0.89 Rd7|0.89 Rd6|0.78 Rd5|0.67 Rc8|0.89 "
            "Ra8|0.89 Rb7|0.89 Rb6|0.78 Rb5|0.67 Rb4|0.56 Rb3|0.45 Rb2|0.34 Rb1|0.23 Ke4|0.89 "
            "Kd4|0.89 Kc4|0.89 Ke3|0.89 Ke2|0.89 Kd2|0.89 Pe6|0.89 Pg5|0.89 Pc4|0.89 ke7|0.89 "
            "kg6|0.89 kg5|0.89 kf5|0.89 ke5|0.89 ba8|0.67 bb7|0.78 bc6|0.89 be4|0.89 bc4|0.89 "
            "bf3|0.78 bb3|0.78 bg2|0.67 ba2|0.67 bh1|0.56 ra6|0.78 ra5|0.89 rg4|0.34 rf4|0.45 "
            "re4|0.56 rd4|0.67 rc4|0.78 rb4|0.89 ra3|0.89 ra2|0.78 ra1|0.67 pf5|0.89 pg6|0.89 "
            "pa6|0.89 pe5|0.89 pc4|0.89 pg5|0.78 pa5|0.78",
            id="Endgame",
        ),
    ],
)
def test_get_activity_encoding(fen_encoding, expected_activity_encoding):
    assert get_activity_encoding(fen_encoding) == expected_activity_encoding


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
def test_get_activity_encoding_invalid_fen(fen_encoding):
    with pytest.raises(ValueError):
        get_activity_encoding(fen_encoding)

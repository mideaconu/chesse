import pytest

from utils.encoding import get_connectivity_encoding


@pytest.mark.parametrize(
    "fen_encoding, expected_connectivity_encoding",
    [
        pytest.param(
            "r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1",
            "N>pe4 B>bc5 b>Be3 R<Qd1 R<Pa2 Q<Ra1 Q<Ke1 Q<Nd2 K<Qd1 K<Bf1 K<Nd2 K<Pf2 B<Pg2 R<Ng1 "
            "R<Ph2 P<Pc3 N<Bf1 P<Be3 B<Nd2 B<Pf2 b<pa7 n<bc5 p<pe6 r<pa7 r<bc8 b<pb7 b<nd7 q<nd7 "
            "q<bc8 q<ke8 k<nd7 k<pf7 k<qd8 r<ph7 r<ng8 R=pa7 R=ra8 Q=nd7 Q=qd8 R=ph7 R=rh8 N=pe4 "
            "B=bc5 B=pa7 b=Be3 b=Pf2 b=Ng1 r=Pa2 r=Ra1 q=Nd2 q=Qd1 r=Ph2 r=Rh1",
            id="Opening",
        ),
        pytest.param(
            "rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -",
            "R>pe7 Q>pa5 Q>pd6 P>pg5 p>Pf4 n>Pd5 b>Pd4 b>Pg4 K<Pb2 K<Pc2 R<Kc1 R<Re2 P<Qa3 P<Nc3 "
            "R<Re1 R<Pc2 R<Bf2 B<Re1 B<Pd4 B<Ph3 B<Pd5 Q<Pa2 Q<Pb2 Q<Nc3 N<Pa2 N<Re2 N<Pd5 P<Pg4 "
            "n<pc4 n<bd7 n<ra8 b<pg5 b<pe7 p<pg5 q<pc4 q<nb6 q<pd6 q<bd7 q<rb8 p<pd6 p<bf6 r<pa5 "
            "r<rb8 r<nb6 r<ra8 r<kg8 k<pf7 R=pe7 R=pe7 B=nb6 B=ra8 Q=pa5 Q=pd6 Q=pe7 Q=ra8 P=pg5 "
            "p=Pf4 n=Pd5 b=Pd4 b=Nc3 b=Pb2 q=Nc3 q=Pc2 q=Kc1 q=Pf4 b=Pg4 b=Ph3 r=Qa3 r=Pa2 r=Pb2",
            id="Middle game",
        ),
        pytest.param(
            "1R1R4/p4pp1/4pk2/2pb1P2/r5Pp/2PK3P/2P5/8 w - - 0 1",
            "r>Pg4 P>pe6 p>Pf5 k>Pf5 R>bd5 P<Kd3 K<Pc2 K<Pc3 P<Pg4 r<pa7 P<Pf5 b<pe6 p<bd5 k<pe6 "
            "k<pf7 k<pg7 p<pe6 p<kf6 R<Rd8 R<Rb8 r=Pg4 P=pe6 p=Pf5 k=Pf5 R=bd5",
            id="Endgame",
        ),
    ],
)
def test_get_connectivity_encoding(fen_encoding, expected_connectivity_encoding):
    assert get_connectivity_encoding(fen_encoding) == expected_connectivity_encoding


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
def test_get_connectivity_encoding_invalid_fen(fen_encoding):
    with pytest.raises(ValueError):
        get_connectivity_encoding(fen_encoding)

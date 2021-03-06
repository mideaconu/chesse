import chess
import pytest
from src.encoding import connectivity_encoding


@pytest.mark.parametrize(
    "board, expected_encoding",
    [
        pytest.param(
            chess.Board(fen="r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1"),
            {"B>bc5", "N>pe4", "b>Be3"},
            id="Opening",
        ),
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            {"P>pg5", "Q>pa5", "Q>pd6", "R>pe7", "b>Pd4", "b>Pg4", "n>Pd5", "p>Pf4"},
            id="Middle game",
        ),
        pytest.param(
            chess.Board(fen="1R1R4/p4pp1/4pk2/2pb1P2/r5Pp/2PK3P/2P5/8 w - - 0 1"),
            {"R>bd5", "P>pe6", "k>Pf5", "r>Pg4", "p>Pf5"},
            id="Endgame",
        ),
    ],
)
def test_get_connectivity_encoding_attack(board, expected_encoding):
    assert connectivity_encoding.encode(board, "attack") == expected_encoding


@pytest.mark.parametrize(
    "board, expected_encoding",
    [
        pytest.param(
            chess.Board(fen="r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1"),
            {
                "K<Bf1",
                "K<Nd2",
                "K<Pf2",
                "K<Qd1",
                "Q<Ke1",
                "Q<Nd2",
                "Q<Ra1",
                "R<Ng1",
                "R<Pa2",
                "R<Ph2",
                "R<Qd1",
                "B<Nd2",
                "B<Pf2",
                "B<Pg2",
                "N<Bf1",
                "P<Be3",
                "P<Pc3",
                "k<nd7",
                "k<pf7",
                "k<qd8",
                "q<bc8",
                "q<ke8",
                "q<nd7",
                "r<bc8",
                "r<ng8",
                "r<pa7",
                "r<ph7",
                "b<nd7",
                "b<pa7",
                "b<pb7",
                "n<bc5",
                "p<pe6",
            },
            id="Opening",
        ),
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            {
                "B<Pd4",
                "B<Pd5",
                "B<Ph3",
                "B<Re1",
                "K<Pb2",
                "K<Pc2",
                "N<Pa2",
                "N<Pd5",
                "N<Re2",
                "P<Nc3",
                "P<Pg4",
                "P<Qa3",
                "Q<Nc3",
                "Q<Pa2",
                "Q<Pb2",
                "R<Bf2",
                "R<Kc1",
                "R<Pc2",
                "R<Re1",
                "R<Re2",
                "b<pe7",
                "b<pg5",
                "k<pf7",
                "n<bd7",
                "n<pc4",
                "n<ra8",
                "p<bf6",
                "p<pd6",
                "p<pg5",
                "q<bd7",
                "q<nb6",
                "q<pc4",
                "q<pd6",
                "q<rb8",
                "r<kg8",
                "r<nb6",
                "r<pa5",
                "r<ra8",
                "r<rb8",
            },
            id="Middle game",
        ),
        pytest.param(
            chess.Board(fen="1R1R4/p4pp1/4pk2/2pb1P2/r5Pp/2PK3P/2P5/8 w - - 0 1"),
            {
                "K<Pc2",
                "K<Pc3",
                "R<Rb8",
                "R<Rd8",
                "P<Kd3",
                "P<Pf5",
                "P<Pg4",
                "b<pe6",
                "k<pe6",
                "k<pf7",
                "k<pg7",
                "r<pa7",
                "p<bd5",
                "p<kf6",
                "p<pe6",
            },
            id="Endgame",
        ),
    ],
)
def test_get_connectivity_encoding_defense(board, expected_encoding):
    assert connectivity_encoding.encode(board, "defense") == expected_encoding


@pytest.mark.parametrize(
    "board, expected_encoding",
    [
        pytest.param(
            chess.Board(fen="r1bqk1nr/pp1n1ppp/4p3/2b5/4p3/2P1B3/PP1N1PPP/R2QKBNR w KQkq - 0 1"),
            {
                "Q=nd7",
                "Q=qd8",
                "R=pa7",
                "R=ph7",
                "R=ra8",
                "R=rh8",
                "B=bc5",
                "B=pa7",
                "N=pe4",
                "q=Nd2",
                "q=Qd1",
                "r=Pa2",
                "r=Ph2",
                "r=Ra1",
                "r=Rh1",
                "b=Be3",
                "b=Ng1",
                "b=Pf2",
            },
            id="Opening",
        ),
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            {
                "B=nb6",
                "B=ra8",
                "P=pg5",
                "Q=pa5",
                "Q=pd6",
                "Q=pe7",
                "Q=ra8",
                "R=pe7",
                "b=Nc3",
                "b=Pb2",
                "b=Pd4",
                "b=Pg4",
                "b=Ph3",
                "n=Pd5",
                "p=Pf4",
                "q=Kc1",
                "q=Nc3",
                "q=Pc2",
                "q=Pf4",
                "r=Pa2",
                "r=Pb2",
                "r=Qa3",
            },
            id="Middle game",
        ),
        pytest.param(
            chess.Board(fen="1R1R4/p4pp1/4pk2/2pb1P2/r5Pp/2PK3P/2P5/8 w - - 0 1"),
            {"R=bd5", "P=pe6", "k=Pf5", "r=Pg4", "p=Pf5"},
            id="Endgame",
        ),
    ],
)
def test_get_connectivity_encoding_ray_attack(board, expected_encoding):
    assert connectivity_encoding.encode(board, "ray-attack") == expected_encoding

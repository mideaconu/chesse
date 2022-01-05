import chess
import pytest

from src.encoding import connectivity_encoding


@pytest.mark.parametrize(
    "board, connection, expected_encoding",
    [
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            "attack",
            {"P>pg5", "Q>pa5", "Q>pd6", "R>pe7", "b>Pd4", "b>Pg4", "n>Pd5", "p>Pf4"},
        ),
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            "defense",
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
        ),
        pytest.param(
            chess.Board(fen="rr4k1/2qbpp2/1n1p1b1p/p2P2p1/2pP1PP1/Q1N4P/PPP1RBB1/2K1R3 w - -"),
            "ray-attack",
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
        ),
    ],
)
def test_get_connectivity_encoding(board, connection, expected_encoding):
    actual_encoding = connectivity_encoding.get_connectivity_encoding(board, connection).split()

    assert len(set(actual_encoding)) == len(actual_encoding)
    assert expected_encoding == set(actual_encoding)

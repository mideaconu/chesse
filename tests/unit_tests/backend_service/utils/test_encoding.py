import pytest

from backend_service.utils import encoding, exception


def test_check_fen_encoding_is_valid():
    fen_encoding = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    encoding.check_fen_encoding_is_valid(fen_encoding)


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
def test_check_fen_encoding_is_valid_fails(fen_encoding):
    with pytest.raises(exception.InvalidFENEncodingError):
        encoding.check_fen_encoding_is_valid(fen_encoding)

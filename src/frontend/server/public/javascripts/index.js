var board = null;

board = Chessboard("search-board", {
    pieceTheme: 'images/chesspieces/default/{piece}.png',
    draggable: true,
    sparePieces: true,
    dropOffBoard: "trash"
});

function searchPosition() {
    console.log(`${board.fen()}`);
    window.location.href = `/search?fen=${board.fen()}`;
}

$('#start-button').on('click', board.start);
$('#clear-button').on('click', board.clear);
$('#flip-button').on('click', board.flip);
$('#search-button').on('click', searchPosition);

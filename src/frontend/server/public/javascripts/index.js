var board = null;

var board_config = {
    pieceTheme: 'images/chesspieces/default/{piece}.png',
    draggable: true,
    sparePieces: true,
    dropOffBoard: "trash",
    showErrors: "alert"
};
board = Chessboard("searchBoard", board_config);

function searchPosition() {
    console.log(`${board.fen()}`);
}

$('#startButton').on('click', board.start);
$('#clearButton').on('click', board.clear);
$('#flipButton').on('click', board.flip);
$('#searchButton').on('click', searchPosition);

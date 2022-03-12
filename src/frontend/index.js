var board = null;
var game = new Chess();

var config = {
  draggable: true,
  sparePieces: true,
  dropOffBoard: "trash"
}

board = Chessboard("searchBoard", config);

function searchPosition() {
    console.log(`Current position: ${board.fen()}`)
}

$('#startButton').on('click', board.start)
$('#clearButton').on('click', board.clear)
$('#searchButton').on('click', searchPosition)

var board = null;
var game = new Chess();

var config = {
  draggable: true,
  sparePieces: true,
  dropOffBoard: "trash"
}

board = Chessboard("searchBoard", config);

$('#startButton').on('click', board.start)
$('#clearButton').on('click', board.clear)

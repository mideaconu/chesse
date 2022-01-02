import chess

def encode(fen: str):
    board = chess.Board(fen=fen)
    print(board)


if __name__ == "__main__":
    encode("r1b2rk1/1pq1ppbp/p2p1np1/3N4/1P2P3/P2B4/2P1NPPP/1R1Q1RK1 b - -")
from chess_const import *

class Chess:
    def __init__(self):
        self.board = []
        self.create_board()
 
    def create_board(self):
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            row = []
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                row.append(EMPTY)
            self.board.append(row)

    def print_board(self):
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                print(self.board[N][M], end=" ")
            print()

chess = Chess()
chess.print_board()
            
        
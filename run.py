from BackEnd.Board import Board
from BackEnd.Piece import Piece
from FrontEnd.GUI import run_game

# 12 cols, 30 rows
# potentially make 12 rows and stack counters???

"""
  | 0 1 2 3 4 5 6 7 8 9 10 11
 ----------------------------
0 | b       w   w           b
1 | b       w   w           b
2 | b       w   w 
3 | b           w
4 | b           w

5 | w           b       
6 | w           b       
7 | w       b   b
8 | w       b   b           w
9 | w       b   b           w

"""

if __name__ == '__main__':
    pieces = []
    pieces.extend([Piece(loc, 'w') for loc in zip([0] * 5, range(5))])
    pieces.extend([Piece(loc, 'b') for loc in zip([0] * 5, range(5, 10))][::-1])

    pieces.extend([Piece(loc, 'b') for loc in zip([4] * 3, range(3))])
    pieces.extend([Piece(loc, 'w') for loc in zip([4] * 3, range(7, 10))][::-1])

    pieces.extend([Piece(loc, 'b') for loc in zip([6] * 5, range(5))])
    pieces.extend([Piece(loc, 'w') for loc in zip([6] * 5, range(5, 10))][::-1])

    pieces.extend([Piece(loc, 'w') for loc in zip([11] * 2, range(2), )])
    pieces.extend([Piece(loc, 'b') for loc in zip([11] * 2, range(8, 10))][::-1])

    board = Board(pieces)
    run_game(board)

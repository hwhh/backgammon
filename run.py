from BackEnd.Board import Board
from BackEnd.Piece import Piece
from FrontEnd.GUI import run_game

# 12 cols, 30 rows
# potentially make 12 rows and stack counters???

"""
  | 0 1 2 3 4 5 6 7 8 9 10 11
 ----------------------------
0 | b       w  | w           b
1 | b       w  | w           b
2 | b       w  | w 
3 | b          | w
4 | b          | w
  | 
4 | w          | b       
3 | w          | b       
2 | w       b  | b
1 | w       b  | b           w
0 | w       b  | b           w
    12 13 
"""

if __name__ == '__main__':
    pieces = []
    pieces.extend([Piece(loc, 'w') for loc in zip([23] * 2, range(2), )])
    pieces.extend([Piece(loc, 'b') for loc in zip([0] * 2, range(2))][::-1])

    pieces.extend([Piece(loc, 'w') for loc in zip([5] * 5, range(5))])
    pieces.extend([Piece(loc, 'b') for loc in zip([18] * 5, range(5))][::-1])

    pieces.extend([Piece(loc, 'b') for loc in zip([16] * 3, range(3))])
    pieces.extend([Piece(loc, 'w') for loc in zip([7] * 3, range(3))][::-1])

    pieces.extend([Piece(loc, 'b') for loc in zip([11] * 5, range(5))])
    pieces.extend([Piece(loc, 'w') for loc in zip([12] * 5, range(5))][::-1])

    board = Board(pieces)
    run_game(board)

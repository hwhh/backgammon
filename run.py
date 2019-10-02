import enum

from BackEnd.Board import Board
from BackEnd.Game import Game
from BackEnd.Piece import Piece


# 12 cols, 30 rows
# potentially make 12 rows and stack counters???


class State(enum.Enum):
    init = 0
    not_rolled = 1
    rolled = 2
    selected = 3
    moved = 4

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
    game = Game()
    game.run()



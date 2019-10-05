import enum
import random
import time

from pygame.threads import Thread

from BackEnd.Board import Board
from BackEnd.Piece import Piece
from FrontEnd.GUI import GUI


class State(enum.Enum):
    init = 0
    not_rolled = 1
    rolled = 2
    selected = 3
    moved = 4


# Not Rolled -> rolled  -> moved
#                       -> blocked -> not rolled


class Game:

    def __init__(self, front_end):
        self.selected_piece = None
        self.state = State.init
        self.turn = None
        self.front_end = front_end
        self.current_die = None, None
        pieces = []
        pieces.extend([Piece(loc, 'w') for loc in zip([23] * 2, range(2), )])
        pieces.extend([Piece(loc, 'b') for loc in zip([0] * 2, range(2))][::-1])  # 1143 - 1098
        pieces.extend([Piece(loc, 'w') for loc in zip([5] * 5, range(5))])
        pieces.extend([Piece(loc, 'b') for loc in zip([18] * 5, range(5))][::-1])
        pieces.extend([Piece(loc, 'b') for loc in zip([16] * 3, range(3))])
        pieces.extend([Piece(loc, 'w') for loc in zip([7] * 3, range(3))][::-1])
        pieces.extend([Piece(loc, 'b') for loc in zip([11] * 5, range(5))])
        pieces.extend([Piece(loc, 'w') for loc in zip([12] * 5, range(5))][::-1])
        self.board = Board(pieces)

    def run(self):
        self.front_end.display_pieces(self.board)
        while not self.game_over():
            time.sleep(0.5)
            event = self.front_end.get_event()

            if event == "Rolled Dice" and self.state.not_rolled:
                die1, die2 = self.roll_dice()

                self.front_end.display_dice(die1, die2)

                # Initial dice roll ro see who goes first
                if self.state == State.init:
                    if die1 > die2:
                        self.turn = 'w'
                        self.state = State.rolled
                    elif die1 < die2:
                        self.turn = 'd'
                        self.state = State.rolled

    def get_turn(self, piece):
        return piece.colour == self.turn

    def game_over(self):
        # self.front_end.set_playing(False)
        return False

    def change_turn(self):
        pass

    def roll_dice(self):
        self.current_die = random.randint(1, 6), random.randint(1, 6)
        return self.current_die

import enum
import random

from BackEnd.Board import Board
from BackEnd.Piece import Piece
from run import State


class Game:

    def __init__(self, front_end):
        self.state = State.init
        self.selected_piece = None
        self.board = None

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

        self.turn = None
        self.front_end = front_end

    def run(self):

        while not self.game_over():
            event = None  # Get event from front end
            if event == init:

    def get_turn(self, piece):
        return piece.colour == self.turn

    def game_over(self):
        return False

    def change_turn(self):
        pass

    def roll_dice(self):
        return random.randint(1, 7), random.randint(1, 7)

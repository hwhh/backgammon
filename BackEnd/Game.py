import enum
import random
import time

from pygame.threads import Thread

from BackEnd.Board import Board
from BackEnd.Piece import Piece
from FrontEnd.GUI import GUI, Action


class State(enum.Enum):
    init = 0
    not_rolled = 1
    rolled = 2
    selected = 3
    moved = 4


class Game:

    def __init__(self, front_end):
        self.board = Board()
        self.front_end = front_end
        self.state = State.init
        self.turn = None
        self.selected_piece = None
        self.current_die = []
        self.history = []

    def transition_function(self, state, action, *args):
        # (Initial state)
        if state == State.init and action == Action.roll:
            self.roll_dice()
            if self.current_die[0] > self.current_die[1]:
                self.turn = 'w'
                return State.rolled
            elif self.current_die[0] < self.current_die[1]:
                self.turn = 'd'
                return State.rolled

        # State rolling dice need to return the dice
        if state == State.not_rolled and action == Action.roll:
            self.roll_dice()
            available_moves = self.board.get_all_available_moves(self.turn, self.current_die[:2])
            if len(available_moves) == 0:
                self.change_turn()
                return State.not_rolled
            return State.rolled, self.current_die[:2]

        # args[0] = piece
        if state == State.rolled and action == Action.select:
            if self.board.pieces[args[0]][-1].colour == self.turn:
                available_moves = self.board.get_available_moves(args[0], self.current_die[:2])
                return State.selected

        # args[0] = piece args[1] = dest
        if state == State.selected and Action == Action.move:
            if args[1] in self.board.get_available_moves(args[0], self.current_die):
                self.current_die.remove(abs(args[0].loc[0] - args[1]))
                if len(self.current_die) == 0 or not self.moves_available():
                    self.change_turn()
                    return State.not_rolled
                else:
                    return State.rolled

        return state

    def moves_available(self):
        return len(self.board.get_all_available_moves(self.turn, self.current_die[:2])) > 0

    def run(self):
        self.front_end.display_pieces(self.board)
        while not self.game_over():
            time.sleep(0.5)
            event = self.front_end.get_event()

    def get_turn(self):
        return self.turn

    def game_over(self):
        return self.board.white_bared_off == 15 or self.board.black_bared_off == 15

    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

    def roll_dice(self):
        die = (random.randint(1, 6), random.randint(1, 6))
        self.current_die = [die[0], die[1]]

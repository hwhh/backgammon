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

    def transition_function(self, state, action):
        # (Initial state)
        if state == State.init and action == Action.roll:
            self.roll_dice()
            self.front_end.display_dice(self.current_die[0], self.current_die[1])
            if self.current_die[0] > self.current_die[1]:
                self.turn = 'w'
                self.front_end.display_turn(self.turn)
                return State.rolled
            elif self.current_die[0] < self.current_die[1]:
                self.turn = 'b'
                self.front_end.display_turn(self.turn)
                return State.rolled

        # State rolling dice need to return the dice
        if state == State.not_rolled and action == Action.roll:
            self.roll_dice()
            available_moves = self.board.get_all_available_moves(self.turn, self.current_die[:2])
            if len(available_moves) == 0:
                self.change_turn()
                return State.not_rolled
            self.front_end.display_dice(self.current_die[0], self.current_die[1])
            return State.rolled

        # args[0] = piece TODO return available moves
        if state == State.rolled and action == Action.select:
            source = self.front_end.get_extras()['source']
            piece = self.board.pieces[source][-1]
            if piece.colour == self.turn:
                available_moves = self.board.get_available_moves(piece, self.current_die[:2])
                return State.selected

        # args[0] = source args[1] = dest
        if state == State.selected and Action == Action.move:
            source = self.front_end.get_extras()['source']
            destination = self.front_end.get_extras()['destination']
            piece = self.board.pieces[source][-1]
            # TODO clear source and destination
            if piece.colour == self.turn and destination in self.board.get_available_moves(piece, self.current_die):
                self.current_die.remove(abs(source - destination))
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
            action = self.front_end.get_action()
            if action is not None:
                self.state = self.transition_function(self.state, action)

    def get_turn(self):
        return self.turn

    def game_over(self):
        return self.board.white_bared_off == 15 or self.board.black_bared_off == 15

    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
        self.front_end.display_turn(self.turn)

    def roll_dice(self):
        die = (random.randint(1, 6), random.randint(1, 6))
        self.current_die = [die[0], die[1]]

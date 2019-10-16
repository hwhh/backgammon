import enum
import random
import logging

from BackEnd.Action import ActionType
from BackEnd.Board import Board


class State(enum.Enum):
    init = 0
    not_rolled = 1
    rolled = 2
    selected = 3
    moved = 4


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


# TODO add undo function
class Game:

    def __init__(self, front_end, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.front_end = front_end
        self.board = Board()
        self.turn = None
        self.selected_piece = None
        self.doubles = False
        self.headless = False
        self.history = []
        self.current_die = []
        self.update_front_end([(self.front_end.set_board, [self.board])])  # TODO
        self.state = State.init

    def transition_function(self, state, action):
        # TODO if selected and invalid move, go back to not selected

        # (Initial state)
        if state == State.init and action.type == ActionType.roll:
            logging.info("State = Init and Action = Roll")
            self.roll_dice()
            while self.current_die[0] == self.current_die[1]:
                self.roll_dice()

            self.update_front_end([(self.front_end.display_dice, [self.current_die[0], self.current_die[1]])])

            if self.current_die[0] > self.current_die[1]:
                logging.info("\t\t White goes first")
                self.turn = 'w'
                self.update_front_end([(self.front_end.display_turn, [self.turn])])
                return State.rolled
            elif self.current_die[0] < self.current_die[1]:
                logging.info("\t\t Black goes first")
                self.turn = 'b'
                self.update_front_end([(self.front_end.display_turn, [self.turn])])
                return State.rolled

        # State rolling dice need to return the dice
        if state == State.not_rolled and action.type == ActionType.roll:
            logging.info("State = Not Rolled and Action = Roll")
            self.roll_dice()
            available_moves = self.board.get_all_available_moves(self.turn, self.current_die[:2])
            if len(available_moves) == 0:
                self.change_turn()
                return State.not_rolled
            self.update_front_end([(self.front_end.display_dice, [self.current_die[0], self.current_die[1]])])
            return State.rolled

        # args[0] = piece TODO fix displaying available moves
        if state == State.rolled and action.type == ActionType.select:
            logging.info("State = Rolled and Action = Select")

            source = action.extras[0]['source']  # TODO this is not correct

            piece = self.board.pieces[source][-1]
            if piece.colour == self.turn:
                logging.info("\t\tPiece selected: " + str(piece.loc))
                available_moves = self.board.get_available_moves(piece, self.current_die[:2])
                self.update_front_end([(self.front_end.highlight_piece, [piece]),
                                       (self.front_end.highlight_moves, [available_moves])])
                return State.selected
            else:
                self.front_end.clear_extras()

        if state == State.rolled and action.type == ActionType.move:
            self.update_front_end([(self.front_end.clear_extras, []),
                                   (self.front_end.remove_highlight_piece, []),
                                   (self.front_end.remove_highlight_moves, [])])

            return State.rolled

        # args[0] = source args[1] = dest
        if state == State.selected and action.type == ActionType.move:
            logging.info("State = Selected and Action = Move")

            source = action.extras[0]['source']
            destination = action.extras[0]['destination']

            piece = self.board.pieces[source][-1]
            available_moves = self.board.get_available_moves(piece, self.current_die)
            if piece.colour == self.turn and destination in available_moves:
                move = abs(source - destination)
                logging.info("\t\tMove was: " + str(move))
                # Find what die combinations where used
                if move in self.current_die:
                    self.current_die.remove(move)
                elif self.doubles:
                    self.current_die = self.current_die[move // self.current_die[0]:]
                else:
                    self.current_die = []

                old_loc = piece.loc
                self.board.move(piece, destination)
                self.history.append(self.board.copy())

                self.update_front_end([(self.front_end.update_piece, [piece, old_loc]),
                                       (self.front_end.clear_extras, []),
                                       (self.front_end.remove_highlight_moves, [])])

                # TODO make the move then check for available moves
                # TODO Add the board to history before making the move
                if len(self.current_die) == 0 or not self.moves_available():
                    self.change_turn()
                    logging.info("\t\tChanged turn.")
                    self.front_end.clear_dice()
                    return State.not_rolled
                else:

                    return State.rolled

            self.update_front_end([(self.front_end.remove_highlight_piece, []),
                                   (self.front_end.remove_highlight_moves, []),
                                   (self.front_end.clear_extras, [])])
            return State.rolled

        # TODO should this be here?
        return state

    def update_front_end(self, funcs):
        if not self.headless:
            for func, args in funcs:
                func(*args)

    def moves_available(self):
        return len(self.board.get_all_available_moves(self.turn, self.current_die[:2])) > 0

    def run(self):
        self.update_front_end([(self.front_end.display_pieces, [])])
        while not self.game_over():
            if self.turn == self.player1.colour:
                action = self.player1.get_action()
            else:
                action = self.player2.get_action()

            if action is not None:
                self.state = self.transition_function(self.state, action)

            # action = self.front_end.get_action()  # TODO this is horrible!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            # if action is not None:
            #     if action.type == ActionType.quit:
            #         break
            #     self.state = self.transition_function(self.state, action)
            #
            #     self.update_front_end([(self.front_end.set_board, [self.board])])

    def get_turn(self):
        return self.turn

    def game_over(self):
        return self.board.white_bared_off == 15 or self.board.black_bared_off == 15

    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
        self.update_front_end([(self.front_end.display_turn, [self.turn])])

    def roll_dice(self):
        die = (random.randint(1, 6), random.randint(1, 6))
        self.current_die = [die[0], die[1]]
        if die[0] == die[1]:
            self.current_die.extend([die[0], die[1]])
            self.doubles = True
        else:
            self.doubles = False

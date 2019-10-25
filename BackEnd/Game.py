import enum
import random
import logging

from BackEnd.Utilities.Action import ActionType
from BackEnd.Board import Board
from BackEnd.Utilities.PlayerEvent import OrEvent
from BackEnd.Utilities.State import State, StateType

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


# TODO add undo function
# TODO at the moment if user uses both die, check intermediate moves to ensure nothing is captured
# TODO you need to make every move, therefore if there is a way to use both die you have to do that
# TODO bug when doubles are rolled can go to jump columns
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
        self.update_front_end([(self.front_end.set_board, [self.board])])
        self.state = State(StateType.init)

    def transition_function(self, state, action):
        # TODO if selected and invalid move, go back to not selected

        # (Initial state)
        if state.type == StateType.init and action.type == ActionType.roll:
            logging.info("State = Init and Action = Roll")
            self.roll_dice()
            while self.current_die[0] == self.current_die[1]:
                self.roll_dice()

            self.update_front_end([(self.front_end.display_dice, [self.current_die[0], self.current_die[1]])])

            if self.current_die[0] > self.current_die[1]:
                logging.info("\t\t White goes first")
                self.turn = 'w'
                self.update_front_end([(self.front_end.display_turn, [self.turn])])
                return State(StateType.rolled)
            elif self.current_die[0] < self.current_die[1]:
                logging.info("\t\t Black goes first")
                self.turn = 'b'
                self.update_front_end([(self.front_end.display_turn, [self.turn])])
                return State(StateType.rolled)

        # State rolling dice need to return the dice
        if state.type == StateType.not_rolled and action.type == ActionType.roll:
            logging.info("State = Not Rolled and Action = Roll")
            self.roll_dice()
            available_moves = self.board.get_all_available_moves(self.turn, self.current_die[:2])
            if len(available_moves) == 0:
                self.change_turn()
                return State(StateType.not_rolled)
            self.update_front_end([(self.front_end.display_dice, [self.current_die[0], self.current_die[1]])])
            return State(StateType.rolled)

        # args[0] = piece TODO fix displaying available moves
        if state.type == StateType.rolled and action.type == ActionType.select:
            logging.info("State = Rolled and Action = Select")

            source = action.extras[0]['source']  # TODO this is not correct

            piece = self.board.pieces[source][-1]
            if piece.colour == self.turn:
                logging.info("\t\tPiece selected: " + str(piece.loc))
                available_moves = self.board.get_available_moves(piece, self.current_die[:2])
                self.update_front_end([(self.front_end.highlight_piece, [piece]),
                                       (self.front_end.highlight_moves, [available_moves])])
                return State(StateType.selected)
            else:
                self.front_end.clear_extras()

        if state.type == StateType.rolled and action.type == ActionType.move:
            self.update_front_end([(self.front_end.clear_extras, []),
                                   (self.front_end.remove_highlight_piece, []),
                                   (self.front_end.remove_highlight_moves, [])])

            return State(StateType.rolled)

        if state.type == StateType.selected and action.type == ActionType.move:
            logging.info("State = Selected and Action = Move")

            source = action.extras[0]['source']
            destination = action.extras[0]['destination']

            piece = self.board.pieces[source][-1]
            available_moves = self.board.get_available_moves(piece, self.current_die)
            if piece.colour == self.turn and destination in available_moves:
                move = abs(source - destination)
                logging.info("\t\tMove was: " + str(move))
                if move in self.current_die:
                    self.current_die.remove(move)
                elif self.doubles:
                    self.current_die = self.current_die[move // self.current_die[0]:]
                else:
                    self.current_die = []

                old_loc = piece.loc
                next_state = self.board.move(piece, destination)

                if next_state.type == StateType.captured:
                    logging.info("\t\t" + str(next_state.extras[0]) + " was captured: ")
                    self.update_front_end([(self.front_end.draw_captured, [next_state.extras[0]])])

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
                    return State(StateType.not_rolled)
                else:

                    return State(StateType.rolled)

            self.update_front_end([(self.front_end.remove_highlight_piece, []),
                                   (self.front_end.remove_highlight_moves, []),
                                   (self.front_end.clear_extras, [])])
            return State(StateType.rolled)

        return state

    def update_front_end(self, funcs):
        if not self.headless:
            for func, args in funcs:
                func(*args)

    def moves_available(self):
        return len(self.board.get_all_available_moves(self.turn, self.current_die[:2])) > 0

    def run(self):
        self.update_front_end([(self.front_end.display_pieces, [])])
        or_e = OrEvent(self.player1.event, self.player2.event)
        while not self.game_over():
            or_e.wait()
            if self.turn == self.player1.colour:
                action = self.player1.get_action()
            else:
                action = self.player2.get_action()
            if action is not None:
                self.state = self.transition_function(self.state, action)
            or_e.clear()

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

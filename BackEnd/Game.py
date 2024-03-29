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
# TODO BUG - somthing wired happens if rolled doubles when tring to bear on - maybe because there were no available moves
# TODO Add notification of no available moves
# TODO make the move then check for available moves
# TODO Add the board to history before making the move
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
        self.or_e = OrEvent(self.player1.event, self.player2.event)

    def transition_function(self, state, action):
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
                self.update_front_end([(self.front_end.display_turn, [self.turn, False])])
                return State(StateType.rolled)
            elif self.current_die[0] < self.current_die[1]:
                logging.info("\t\t Black goes first")
                self.turn = 'b'
                self.update_front_end([(self.front_end.display_turn, [self.turn, False])])
                return State(StateType.rolled)

        # State rolling dice need to return the dice
        if state.type == StateType.not_rolled and action.type == ActionType.roll:
            logging.info("State = Not Rolled and Action = Roll")
            self.roll_dice()
            available_moves = self.board.get_all_available_moves(self.turn, self.current_die[
                                                                            :2])  # TODO this is calculated twice, here and bellow - could just do it once?
            self.update_front_end([(self.front_end.display_dice, [self.current_die[0], self.current_die[1]])])
            if len(available_moves) == 0:
                # TODO display no moves
                logging.info("\t\tNo more available moves - switching turn")
                self.change_turn()
                self.current_die = []
                self.update_front_end([(self.front_end.clear_extras, []),
                                       (self.front_end.clear_dice, [])])

                return State(StateType.not_rolled)
            return State(StateType.rolled, available_moves)

        if state.type == StateType.rolled and action.type == ActionType.select:
            logging.info("State = Rolled and Action = Select")
            source = action.extras[0]['source']
            piece = None
            if len(self.board.black_captured) >= 0 and source == 24:  # black trying to bear on
                piece = self.board.black_captured[-1]
            elif len(self.board.white_captured) >= 0 and source == 25:  # white trying to bear on
                piece = self.board.white_captured[-1]
            elif (len(self.board.white_captured) == 0 and self.turn == 'w') or (
                    len(self.board.black_captured) == 0 and self.turn == 'b'):
                piece = self.board.pieces[source][-1]
            if piece is not None and piece.colour == self.turn:
                logging.info("\t\tPiece selected: " + str(piece.loc))
                available_moves = self.board.get_available_moves(piece, self.current_die)
                if len(state.extras) == 0 or (
                        len(state.extras) > 0 and set(available_moves).issubset(set(state.extras[0]))):
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
            piece, source = self.get_source(action.extras[0]['source'])
            dest = action.extras[0]['destination']
            available_moves = self.board.get_available_moves(piece, self.current_die)
            if piece.colour == self.turn and dest in available_moves:
                move = abs(source - 24) if dest == 26 else abs(source - (-1)) if dest == 27 else abs(source - dest)
                logging.info("\t\tMove was: " + str(move))
                history = {'turn': self.turn,
                           'board': self.board.copy(),
                           'dice': self.current_die.copy(),
                           'moved_piece': piece,
                           'captured': False
                           }

                self.update_dice(move)
                old_loc = piece.loc
                next_state = self.board.move(piece, dest)
                if next_state.type == StateType.captured:
                    logging.info("\t\t" + str(next_state.extras[0]) + " was captured: ")
                    history['captured'] = True
                    self.update_front_end([(self.front_end.draw_captured, [next_state.extras[0]])])

                self.update_front_end([(self.front_end.update_piece, [piece, old_loc]),
                                       (self.front_end.clear_extras, []),
                                       (self.front_end.remove_highlight_moves, [])])
                self.history.append(history)
                if len(self.current_die) == 0 or not self.moves_available():
                    self.change_turn()
                    logging.info("\t\tChanged turn to: " + str(self.turn))
                    self.update_front_end([(self.front_end.clear_dice, [])])
                    return State(StateType.not_rolled)
                else:
                    return State(StateType.rolled)

            self.update_front_end([(self.front_end.remove_highlight_piece, []),
                                   (self.front_end.remove_highlight_moves, []),
                                   (self.front_end.clear_extras, [])])
            return State(StateType.rolled)

        return state

    def get_source(self, source):
        if source == 24:
            return self.board.black_captured[-1], -1
        elif source == 25:
            return self.board.white_captured[-1], 24
        else:
            return self.board.pieces[source][-1], source

    def update_dice(self, move):
        if move in self.current_die:
            self.current_die.remove(move)
        elif self.doubles:
            if self.current_die[0] > move:  # This is likely a finishing move
                self.current_die.pop()
            else:
                self.current_die = self.current_die[move // self.current_die[0]:]
        elif len(self.current_die) > 0 and any(die > move for die in self.current_die):
            self.current_die.pop(self.current_die.index(max(self.current_die)))
        else:
            self.current_die = []

    def update_front_end(self, funcs):
        if not self.headless:
            for func, args in funcs:
                func(*args)

    def moves_available(self):
        return len(self.board.get_all_available_moves(self.turn, self.current_die[:2])) > 0

    def run(self):
        self.update_front_end([(self.front_end.display_pieces, [])])
        while not self.game_over():
            self.or_e.wait()
            if self.turn == self.player1.colour:
                action = self.player1.get_action()
            else:
                action = self.player2.get_action()
            if action is not None:
                self.state = self.transition_function(self.state, action)
            self.or_e.clear()

    def undo(self):
        previous_state = self.history.pop()
        self.current_die = previous_state['dice']
        self.turn = previous_state['turn']
        self.board = previous_state['board']
        self.update_front_end([()])
        self.update_front_end([(self.front_end.update_piece, [previous_state['piece'], old_loc]),
                               (self.front_end.clear_extras, []),
                               (self.front_end.remove_highlight_moves, [])])

    def get_turn(self):
        return self.turn

    def game_over(self):
        if len(self.board.black_bared_off) == 15:
            logging.info('Black wins!')
            self.update_front_end([(self.front_end.display_turn, [self.turn, True])])
            return True
        if len(self.board.white_bared_off) == 15:
            logging.info('White wins!')
            self.update_front_end([(self.front_end.display_turn, [self.turn, True])])
            return True
        return False

    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
        self.update_front_end([(self.front_end.display_turn, [self.turn, False])])

    def roll_dice(self):
        die = (random.randint(1, 6), random.randint(1, 6))
        self.current_die = [die[0], die[1]]
        if die[0] == die[1]:
            self.current_die.extend([die[0], die[1]])
            self.doubles = True
        else:
            self.doubles = False

import copy
import functools
import itertools
import operator

from BackEnd.Piece import Piece
from BackEnd.Utilities.State import StateType, State


class Board:

    # A list of stacks

    def __init__(self):
        self.pieces = [[] for _ in range(24)]

        self.black_bared_off = 0
        self.black_captured = []
        self.white_bared_off = 0
        self.white_captured = []
        self.initialise_board()

    def initialise_board(self):
        pieces = []
        # pieces.extend([Piece(loc, 'w') for loc in zip([23] * 2, range(2))])
        # pieces.extend([Piece(loc, 'b') for loc in zip([0] * 2, range(2))])
        #
        # pieces.extend([Piece(loc, 'w') for loc in zip([5] * 5, range(5))])
        # pieces.extend([Piece(loc, 'b') for loc in zip([18] * 5, range(5))])
        # pieces.extend([Piece(loc, 'b') for loc in zip([16] * 3, range(3))])
        # pieces.extend([Piece(loc, 'w') for loc in zip([7] * 3, range(3))])
        # pieces.extend([Piece(loc, 'b') for loc in zip([11] * 5, range(5))])
        # pieces.extend([Piece(loc, 'w') for loc in zip([12] * 5, range(5))])
        pieces.extend([Piece(loc, 'w') for loc in zip([0] * 2, range(2))])
        pieces.extend([Piece(loc, 'w') for loc in zip([1] * 5, range(5))])
        pieces.extend([Piece(loc, 'w') for loc in zip([2] * 3, range(3))])
        pieces.extend([Piece(loc, 'w') for loc in zip([5] * 5, range(5))])

        pieces.extend([Piece(loc, 'b') for loc in zip([23] * 2, range(2))])
        pieces.extend([Piece(loc, 'b') for loc in zip([22] * 5, range(5))])
        pieces.extend([Piece(loc, 'b') for loc in zip([21] * 3, range(3))])
        pieces.extend([Piece(loc, 'b') for loc in zip([20] * 5, range(5))])
        for piece in pieces:
            self.pieces[piece.loc[0]].append(piece)

    def get_pieces(self):
        return [piece for piece in itertools.chain.from_iterable(self.pieces)]

    def can_bear_off_piece(self, piece, dest):
        if piece.colour == 'b':
            if piece.colour == 'b' and len(self.black_captured) > 0:
                return False
            if dest > 24 and sum([len(x) for x in self.pieces[18:piece.loc[0]]]) > 0:  #
                return False
            for row in self.pieces[:19]:
                if len(row) > 0 and row[-1].colour == 'b':
                    return False
        if piece.colour == 'w':
            if piece.colour == 'w' and len(self.white_captured) > 0:
                return False
            if dest < -1 and sum([len(x) for x in self.pieces[piece.loc[0] + 1:6]]) > 0:  #
                return False
            for row in self.pieces[6:]:
                if len(row) > 0 and row[-1].colour == 'w':
                    return False
        return True

    def move(self, piece, destination):
        state = State(StateType.moved)

        if destination == 26 or destination == 27:
            pass
        elif len(self.pieces[destination]) > 0:
            if self.pieces[destination][-1].colour != piece.colour:
                self.pieces[destination][-1].captured = True
                state = State(StateType.captured, self.pieces[destination][-1])
                if self.pieces[destination][-1].colour == 'b':
                    self.pieces[destination][-1].loc = (24, len(self.black_captured))
                    self.black_captured.append(self.pieces[destination].pop())
                elif self.pieces[destination][-1].colour == 'w':
                    self.pieces[destination][-1].loc = (25, len(self.white_captured))
                    self.white_captured.append(self.pieces[destination].pop())
        if piece.loc[0] == 24:
            self.pieces[destination].append(self.black_captured.pop())
        elif piece.loc[0] == 25:
            self.pieces[destination].append(self.white_captured.pop())
        else:
            self.pieces[destination].append(self.pieces[piece.loc[0]].pop())

        piece.move((destination, len(self.pieces[destination]) - 1))
        return state

    @staticmethod
    def get_destinations(piece, dice):
        destinations = [None, None, None, None]

        def get_destinations_for_colour(operator):
            destinations[0] = operator(piece.loc[0], dice[0])
            if len(dice) > 1:
                if len(dice) > 2:  # This means doubles
                    for i, die in enumerate(dice):
                        destinations[i] = operator(piece.loc[0], (dice[0] * (i + 1)))
                else:
                    destinations[1] = operator(piece.loc[0], dice[1])
                    destinations[2] = operator(piece.loc[0], (dice[0] + dice[1]))

        if piece.colour == 'w':
            get_destinations_for_colour(lambda x, y: (x - y))
        elif piece.colour == 'b':
            get_destinations_for_colour(lambda x, y: (x + y))
        return destinations[0], destinations[1], destinations[2], destinations[3]

    def validate_move(self, piece, dest):
        if 0 <= dest <= 23 and (len(self.pieces[dest]) <= 1 or (self.pieces[dest][-1]).colour == piece.colour):
            return True
        if self.can_bear_off_piece(piece, dest):
            return True
        return False

    def get_available_moves(self, piece, dice):  # TODO check for doubles
        available_moves = []
        dest1, dest2, dest3, dest4 = self.get_destinations(piece, dice)
        if len(self.white_captured) > 0 and piece.colour == 'w':
            if self.white_captured[-1] != piece:
                return []
            return self.get_bear_on_moves(dice, piece.colour)
        elif len(self.black_captured) > 0 and piece.colour == 'b':
            if self.black_captured[-1] != piece:
                return []
            return self.get_bear_on_moves(dice, piece.colour)
        else:
            m1_available, m2_available, m3_available = False, False, False
            if self.validate_move(piece, dest1):
                m1_available = True
                available_moves.append(dest1)
            if dest2 is not None and self.validate_move(piece, dest2):
                if len(dice) > 1 and ((dice[0] != dice[1]) or (dice[0] == dice[1] and m1_available)):
                    m2_available = True
                    available_moves.append(dest2)
            if dest3 is not None and self.validate_move(piece, dest3):
                if ((m1_available or m2_available) and dice[0] != dice[1]) or (m1_available and m2_available):
                    available_moves.append(dest3)
                    m3_available = True
            if dest4 is not None and self.validate_move(piece, dest4):
                if m3_available:
                    available_moves.append(dest4)
        return set([self.get_destination(x) for x in available_moves])

    @staticmethod
    def get_destination(value):
        if value < 0:
            return 27
        elif value > 23:
            return 26
        return value

    def get_bear_on_moves(self, dice, colour):
        all_available_moves = []
        if len(self.black_captured) >= 1 and colour == 'b':
            for die in set(dice):
                if len(self.pieces[die - 1]) <= 1 or self.pieces[die - 1][-1].colour == 'b':
                    all_available_moves.append(die - 1)
        elif len(self.white_captured) >= 1 and colour == 'w':
            for die in set(dice):
                if len(self.pieces[24 - die]) <= 1 or self.pieces[24 - die][-1].colour == 'w':
                    all_available_moves.append(24 - die)
        return all_available_moves

    def get_all_available_moves(self, colour, dice):
        if (len(self.black_captured) > 0 and colour == 'b') or (len(self.white_captured) > 0 and colour == 'w'):
            all_available_moves = self.get_bear_on_moves(dice, colour)
        else:
            all_available_moves = []
            multiple_moves = 0
            current_index, last_index = -1, 0
            for i, col in enumerate(self.pieces):
                if len(col) > 0 and col[-1].colour == colour:
                    all_available_moves.append(self.get_available_moves(col[-1], dice))
                    if len(all_available_moves[current_index]) > 1:
                        multiple_moves += 1
                        last_index = current_index
                    current_index += 1

            if multiple_moves == 1 and len(all_available_moves) > 1:
                return all_available_moves[last_index]
            else:
                return functools.reduce(operator.iconcat, all_available_moves, [])

        return set(all_available_moves)

    def copy(self):
        board = Board()
        board.pieces = copy.deepcopy(self.pieces)
        board.black_bared_off = self.black_bared_off
        board.black_bared_off = self.white_bared_off
        return board

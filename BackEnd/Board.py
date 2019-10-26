import copy
import itertools

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
        pieces.extend([Piece(loc, 'w') for loc in zip([23] * 2, range(2))])
        pieces.extend([Piece(loc, 'b') for loc in zip([0] * 2, range(2))])
        pieces.extend([Piece(loc, 'w') for loc in zip([5] * 5, range(5))])
        pieces.extend([Piece(loc, 'b') for loc in zip([18] * 5, range(5))])
        pieces.extend([Piece(loc, 'b') for loc in zip([16] * 3, range(3))])
        pieces.extend([Piece(loc, 'w') for loc in zip([7] * 3, range(3))])
        pieces.extend([Piece(loc, 'b') for loc in zip([11] * 5, range(5))])
        pieces.extend([Piece(loc, 'w') for loc in zip([12] * 5, range(5))])
        for piece in pieces:
            self.pieces[piece.loc[0]].append(piece)

    def get_pieces(self):
        return [piece for piece in itertools.chain.from_iterable(self.pieces)]

    def move(self, piece, destination):
        state = State(StateType.moved)
        if len(self.pieces[destination]) > 0:
            if self.pieces[destination][-1].colour != piece.colour:
                self.pieces[destination][-1].captured = True
                state = State(StateType.captured, self.pieces[destination][-1])
                if self.pieces[destination][-1].colour == 'b':
                    self.pieces[destination][-1].loc = (24, len(self.black_captured))
                    self.black_captured.append(self.pieces[destination].pop())
                elif self.pieces[destination][-1].colour == 'w':
                    self.pieces[destination][-1].loc = (25, len(self.white_captured))
                    self.white_captured.append(self.pieces[destination].pop())
        self.pieces[destination].append(self.pieces[piece.loc[0]].pop())
        piece.move((destination, len(self.pieces[destination]) - 1))
        return state

    def can_bear_off(self):
        pass

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

    def get_available_moves(self, piece, dice):  # TODO check for doubles
        available_moves = []
        dest1, dest2, dest3, dest4 = self.get_destinations(piece, dice)
        if self.can_bear_off():
            pass

        elif len(self.white_captured) > 0 and piece.colour == 'w':
            if self.white_captured[-1] != piece:
                return []
            return self.get_bear_on_moves(dice, piece.colour)
        elif len(self.black_captured) > 0 and piece.colour == 'b':
            if self.black_captured[-1] != piece:
                return []
            return self.get_bear_on_moves(dice, piece.colour)

        else:
            m1_available, m2_available, m3_available = False, False, False
            if 0 <= dest1 <= 23 and (len(self.pieces[dest1]) <= 1 or (self.pieces[dest1][-1]).colour == piece.colour):
                m1_available = True
                available_moves.append(dest1)
            if dest2 is not None and 0 <= dest2 <= 23 and (
                    len(self.pieces[dest2]) <= 1 or (self.pieces[dest2][-1]).colour == piece.colour):
                m2_available = True
                available_moves.append(dest2)
            if dest3 is not None and 0 <= dest3 <= 23 and (
                    len(self.pieces[dest3]) <= 1 or (self.pieces[dest3][-1]).colour == piece.colour):
                if ((m1_available or m2_available) and dice[0] != dice[1]) or (m1_available and m2_available):
                    available_moves.append(dest3)
                    m3_available = True
            if dest4 is not None and 0 <= dest4 <= 23 and (
                    len(self.pieces[dest4]) <= 1 or (self.pieces[dest4][-1]).colour == piece.colour):
                if m3_available:
                    available_moves.append(dest4)
        return set(available_moves)

    def get_bear_on_moves(self, dice, colour):
        all_available_moves = []
        if len(self.black_captured) >= 1 and colour == 'b':
            for die in set(dice):
                if len(self.pieces[die - 1]) <= 1 or self.pieces[die - 1][-1].colour == 'b':
                    all_available_moves.append(die)
        elif len(self.white_captured) >= 1 and colour == 'w':
            for die in set(dice):
                if len(self.pieces[24 - die]) <= 1 or self.pieces[24 - die][-1].colour == 'w':
                    all_available_moves.append(die)

        return all_available_moves

    def get_all_available_moves(self, colour, dice):
        if (len(self.black_captured) > 0 and colour == 'b') or (len(self.white_captured) > 0 and colour == 'w'):
            all_available_moves = self.get_bear_on_moves(dice, colour)
        else:
            all_available_moves = []
            for col in self.pieces:
                if len(col) > 0 and col[-1].colour == colour:
                    all_available_moves.extend(self.get_available_moves(col[-1], dice))

        return set(all_available_moves)

    def bear_off(self):
        pass

    def bear_on(self):
        pass

    def capture(self):
        pass

    def captured(self):
        pass

    def copy(self):
        board = Board()
        board.pieces = copy.deepcopy(self.pieces)
        board.black_bared_off = self.black_bared_off
        board.black_bared_off = self.white_bared_off
        return board

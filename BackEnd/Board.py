import copy
import itertools

from BackEnd.Piece import Piece


class Board:

    # A list of stacks

    def __init__(self):
        self.pieces = [[] for _ in range(24)]
        self.black_bared_off = 0
        self.black_captured = 0
        self.white_bared_off = 0
        self.white_captured = 0
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
        if len(self.pieces[destination][-1]) > 0:
            if self.pieces[destination][-1] != piece.colour:
                if self.pieces[destination][-1] == 'b':
                    self.black_captured += 1
                elif self.pieces[destination][-1] == 'w':
                    self.white_captured += 1
                self.pieces[destination][-1].captured = True
            return "capture"

        self.pieces[destination].append(self.pieces[piece.loc[0]].pop())
        piece.move((destination, len(self.pieces[destination]) - 1))

    def can_bear_off(self):
        return False

    def get_destinations(self, piece, die):
        dest1, dest2, dest3, dest4 = None, None, None, None
        if piece.colour == 'w':
            dest1 = piece.loc[0] - die[0]
            if len(die) > 1:
                dest2 = piece.loc[0] - die[1]
                dest3 = piece.loc[0] - (die[0] + die[1])
                if die[0] == die[1]:
                    dest4 = piece.loc[0] - (die[0] * 4)
        elif piece.colour == 'b':
            dest1 = piece.loc[0] + die[0]
            if len(die) > 1:
                dest2 = piece.loc[0] + die[1]
                dest3 = piece.loc[0] + (die[0] + die[1])
                if die[0] == die[1]:
                    dest4 = piece.loc[0] + (die[0] * 4)
        return dest1, dest2, dest3, dest4

    def get_available_moves(self, piece, dice):  # TODO check for doubles
        available_moves = []
        dest1, dest2, dest3, dest4 = self.get_destinations(piece, dice)
        if self.can_bear_off():
            pass
        elif self.captured():
            pass
        else:
            m1_available, m2_available = False, False
            if 0 <= dest1 <= 23 and (len(self.pieces[dest1]) <= 1 or (self.pieces[dest1][-1]).colour == piece.colour):
                m1_available = True
                available_moves.append(dest1)
            if dest2 is not None and 0 <= dest2 <= 23 and (
                    len(self.pieces[dest2]) <= 1 or (self.pieces[dest2][-1]).colour == piece.colour):
                m2_available = True
                available_moves.append(dest2)
            if dest3 is not None and 0 <= dest3 <= 23 and (
                    len(self.pieces[dest3]) <= 1 or (self.pieces[dest3][-1]).colour == piece.colour):
                if m1_available or m2_available:
                    available_moves.append(dest3)
            if dest4 is not None and 0 <= dest4 <= 23 and (
                    len(self.pieces[dest4]) <= 1 or (self.pieces[dest4][-1]).colour == piece.colour):
                available_moves.append(dest4)
        return set(available_moves)

    def get_all_available_moves(self, colour, dice):
        all_available_moves = []

        if self.black_captured >= 1 and colour == 'b':
            pass
        elif self.white_captured >= 1 and colour == 'w':
            pass

        else:
            for col in self.pieces:
                if len(col) > 0 and col[-1].colour == colour:
                    all_available_moves.extend(self.get_available_moves(col[-1], dice))
            return all_available_moves

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

import itertools


class Board:

    # A list of stacks

    def __init__(self, pieces):
        self.pieces = [[] for i in range(24)]
        for piece in pieces:
            self.pieces[piece.loc[0]].append(piece)

    def get_pieces(self):
        return [piece for piece in itertools.chain.from_iterable(self.pieces)]

    def move(self, source, destination):
        if source[1] < 5:
            return (self.pieces[source[0]][-1]).loc == source
        else:
            return (self.pieces[source[0] + 12][-1]).loc == source

    def can_bear_off(self):
        return False

    def get_destinations(self, piece, die):
        dest1, dest2, dest3, dest4 = None, None, None, None
        if piece.colour == 'b':
            dest1, dest2 = piece.loc[0] - die[0], piece.loc[0] - die[1]
            dest3 = piece.loc[0] - (die[0] + die[1])
            if die[0] == die[1]:
                dest4 = piece.loc[0] - (die[0] * 4)
        elif piece.colour == 'w':
            dest1, dest2 = piece.loc[0] + die[0], piece.loc[0] + die[1]
            dest3 = piece.loc[0] + (die[0] + die[1])
            if die[0] == die[1]:
                dest4 = piece.loc[0] + (die[0] * 4)
        return dest1, dest2, dest3, dest4

    def get_available_moves(self, piece, die):  # TODO check for doubles
        available_moves = []
        dest1, dest2, dest3, dest4 = self.get_destinations(piece, die)
        if self.can_bear_off():
            pass
        else:
            m1_available, m2_available = False, False
            if 0 <= dest1 <= 23 and (len(self.pieces[dest1]) <= 1 or (self.pieces[dest1][-1]).colour == piece.colour):
                m1_available = True
                available_moves.append(dest1)
            if 0 <= dest2 <= 23 and (len(self.pieces[dest2]) <= 1 or (self.pieces[dest2][-1]).colour == piece.colour):
                m2_available = True
                available_moves.append(dest2)
            if 0 <= dest3 <= 23 and (len(self.pieces[dest3]) <= 1 or (self.pieces[dest3][-1]).colour == piece.colour):
                if m1_available or m2_available:
                    available_moves.append(dest3)
            if dest4 is not None and 0 <= dest4 <= 23 and (
                    len(self.pieces[dest4]) <= 1 or (self.pieces[dest4][-1]).colour == piece.colour):
                available_moves.append(dest4)

        return list(set(available_moves))

    def bear_off(self):
        pass

    def bear_on(self):
        pass

    def capture(self):
        pass

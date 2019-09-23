import itertools


class Board:

    # A list of stacks

    def __init__(self, pieces):
        self.pieces = [[] for i in range(24)]
        for piece in pieces:
            index = piece.loc[0]
            if piece.loc[1] >= 5:
                self.pieces[(index + 12)].append(piece)
            else:
                self.pieces[index].append(piece)

    def get_pieces(self):
        return [piece for piece in itertools.chain.from_iterable(self.pieces)]

    def move(self, source, destination):
        if source[1] < 5:
            return (self.pieces[source[0]][-1]).loc == source
        else:
            return (self.pieces[source[0] + 12][-1]).loc == source

    def bear_off(self):
        pass

    def bear_on(self):
        pass

    def capture(self):
        pass

    def can_bear_off(self, player):
        pass

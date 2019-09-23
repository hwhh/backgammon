class Piece:

    def __init__(self, loc, colour):
        self.loc = loc
        self.colour = colour
        self.captured = False
        self.out = False
        self.selected = False

    def __eq__(self, other):
        return self.loc[0] == other.loc[0] and self.loc[1] == other.loc[1]

    def get_available_moves(self, dice):
        pass

    def captured(self):
        return self.captured

    def home(self):
        return self.home

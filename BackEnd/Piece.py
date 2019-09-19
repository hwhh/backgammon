class Piece:

    def __init__(self, board_location, colour):
        self.board_location = board_location
        self.colour = colour
        self.captured = False
        self.out = False

    def get_available_moves(self, dice):
        pass

    def captured(self):
        return False

    def home(self):
        return False

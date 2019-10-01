class Game:

    def __init__(self):
        self.turn = None

    def get_turn(self, piece):
        return piece.colour == self.turn

    def game_over(self):
        return False

    def change_turn(self):
        pass

    def roll_dice(self):
        pass

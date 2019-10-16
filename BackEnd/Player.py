class Player:

    def __init__(self, colour):
        self.colour = colour

        self.action = None
        # self.front_end = front_end

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action

    def get_colour(self):
        return self.colour

    def roll_dice(self):
        pass

    def bear_off(self):
        pass

    def move(self):
        pass

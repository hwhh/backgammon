import threading


class Player:

    def __init__(self, colour):
        self.colour = colour
        self.event = threading.Event()
        self.action = None

    def set_action(self, action):
        self.action = action
        self.event.set()

    def get_action(self):
        self.event.clear()
        action = self.action
        self.action = None
        return action

    def get_colour(self):
        return self.colour



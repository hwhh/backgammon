from enum import Enum


class ActionType(Enum):
    roll = 0
    select = 1
    move = 2
    quit = -1


class Action:

    def __init__(self, action_type, *extras):
        self.type = action_type
        self.extras = extras

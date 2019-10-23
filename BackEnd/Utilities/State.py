from enum import Enum


class StateType(Enum):
    init = 0
    not_rolled = 1
    rolled = 2
    selected = 3
    moved = 4
    captured = 5
    bear_on = 6
    bear_off = 7

class State:

    def __init__(self, state_type, *extras):
        self.type = state_type
        self.extras = extras

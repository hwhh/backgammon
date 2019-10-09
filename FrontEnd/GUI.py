import enum
import math
import queue

import pygame, random, time
from pygame import font

WHITE = (255, 255, 255)
WOOD = (200, 200, 150)
BLACK = (0, 0, 0)


class Action(enum.Enum):
    roll = 0
    select = 1
    move = 2


class GUI:

    def __init__(self):
        pygame.init()
        res = (1200, 824)
        self.action = None
        self.playing = True
        self.extras = {}
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(res)
        self.background = pygame.transform.smoothscale(pygame.image.load('./Assets/board.png').convert(), res)

    @staticmethod
    def pos_to_screen(board_location, distance):
        if board_location[0] < 6:
            x, y = abs((board_location[0] * 90) - 1120), (765 - (distance * (board_location[1])))
        elif 6 <= board_location[0] < 12:
            x, y = abs((board_location[0] * 90) - 1065), (765 - (distance * (board_location[1])))
        elif 12 <= board_location[0] < 17:
            x, y = abs((abs(board_location[0] - 23) * 90) - 1065), (distance * (board_location[1] + 1))
        else:
            x, y = abs((abs(board_location[0] - 23) * 90) - 1120), (distance * (board_location[1] + 1))

        # TODO draw number of counters stacked at this point
        # TODO fix bug with distance shifting the counter off the edge of board

        if board_location[0] <= 11 and y < 420:
            y = 420
        if board_location[0] > 11 and y > 400:
            y = 400
        return x, y

    @staticmethod
    def screen_to_pos(event):
        x = None
        for i in range(12):
            if i < 6 and (1120 - (i * 90)) - 25 <= event.pos[0] <= (1120 - (i * 90)) + 25:
                x = i
                break
            elif i >= 6 and (1065 - (i * 90)) - 25 <= event.pos[0] <= (1065 - (i * 90)) + 25:
                x = i
                break
        if event.pos[1] <= 400:
            x = 23 - x
        return x

    @staticmethod
    def dice_rolled(event):
        return 575 <= event.pos[0] <= 622 and 790 <= event.pos[1] <= 820

    @staticmethod
    def calculate_spacing(x, board):
        if len(board.pieces[x]) <= 5:
            return 50
        else:
            return int(round(50 - (len(board.pieces[x]) * 1.5)))

    def piece_selected(self, x, event, board):
        if x is None:
            return False
        else:
            dis = self.calculate_spacing(x, board)
            if x > 11 and event.pos[1] < 410:
                return (dis * len(board.pieces[x]) - 25) <= event.pos[1] <= (
                        dis * len(board.pieces[x]) + 25)
            else:
                return (790 - (dis * len(board.pieces[x]))) <= event.pos[1] <= (
                        840 - (dis * len(board.pieces[x])))

    def set_playing(self, playing):
        self.playing = playing

    def display_dice(self, die1, die2):
        # TODO if doubles display 4 dice
        pygame.draw.rect(self.display, WHITE, (540, 420, 40, 40))
        self.display.blit(pygame.font.SysFont('Arial', 25).render(str(die1), True, (0, 0, 0)), (555, 435))
        pygame.draw.rect(self.display, WHITE, (600, 420, 40, 40))
        self.display.blit(pygame.font.SysFont('Arial', 25).render(str(die2), True, (0, 0, 0)), (615, 435))
        pygame.display.update()

    def display_pieces(self, board):

        for piece in board.get_pieces():
            location = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0], board))
            pygame.draw.circle(self.background, WOOD if piece.colour == 'w' else BLACK, location, 25)
        # TODO bug where roll button has to be displayed here
        self.display.blit(self.background, (0, 0))
        pygame.draw.rect(self.display, WHITE, (575, 790, 47, 30))
        self.display.blit(pygame.font.SysFont('Arial', 25).render('Roll', True, (0, 0, 0)), (583, 800))

        pygame.display.update()

    def display_turn(self, turn):
        # self.display.blit(self.background, (0, 0))
        if turn == 'w':
            self.display.blit(pygame.font.SysFont('Arial', 25).render('White\'s Go', True, (0, 0, 0)), (562, 8))
        elif turn == 'b':
            self.display.blit(pygame.font.SysFont('Arial', 25).render('Black\'s Go', True, (0, 0, 0)), (562, 8))
        pygame.display.update()

    def get_action(self):
        action = self.action
        self.action = None
        return action

    def get_extras(self):
        return self.extras

    def run(self):
        running = True
        while self.playing and running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # TODO encode into the state the source and only store thr last click.
                    # I.E. if the state is selected and then another click is fired assume this
                    # click is the destination. Therefore the source click location need to be saved
                    # in the "selected" state object

                    if event.button == 1 and self.dice_rolled(event):
                        self.action = Action.roll

                    elif event.button == 1 and self.screen_to_pos(event) is not None:
                        self.action = Action.select
                        self.extras["source"] = self.screen_to_pos(event)

                    elif event.button == 1 and self.screen_to_pos(event) is None:
                        self.action = Action.move
                        if "source" in self.extras:
                            self.extras["destination"] = self.screen_to_pos(event)

                if event.type == pygame.QUIT:
                    running = False

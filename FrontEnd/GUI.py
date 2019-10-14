import enum
import math
import queue

import pygame, random, time
from pygame import font

WHITE = (255, 255, 255)
WOOD = (200, 200, 150)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)


class Action(enum.Enum):
    roll = 0
    select = 1
    move = 2


# TODO after the event has taken place and board is updated hand back the board

class GUI:

    def __init__(self):
        pygame.init()
        res = (1200, 824)
        self.board = None
        self.action = None
        self.playing = True
        self.extras = {}
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(res)
        self.background = pygame.transform.smoothscale(pygame.image.load('./Assets/board.png').convert(), res)
        rect1 = self.display.blit(self.background, (0, 0))
        rect2 = pygame.draw.rect(self.display, WHITE, (575, 790, 47, 30))
        rect3 = self.display.blit(pygame.font.SysFont('Arial', 25).render('Roll', True, (0, 0, 0)), (583, 800))
        pygame.display.update([rect1, rect2, rect3])

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

    def get_action(self):
        action = self.action
        self.action = None
        return action

    def get_extras(self):
        return self.extras

    def clear_extras(self):
        self.extras = None

    def set_board(self, board):
        self.board = board

    def set_playing(self, playing):
        self.playing = playing

    def piece_selected(self, x, event):
        if x is None:
            return False
        else:
            dis = self.calculate_spacing(x, self.board)
            if x > 11 and event.pos[1] < 410:
                return (dis * len(self.board.pieces[x]) - 25) <= event.pos[1] <= (
                        dis * len(self.board.pieces[x]) + 25)
            else:
                return (790 - (dis * len(self.board.pieces[x]))) <= event.pos[1] <= (
                        840 - (dis * len(self.board.pieces[x])))

    def show_available_moves(self, available_moves):
        pass
        # for move in available_moves:
        #     x, y = self.pos_to_screen((move, 0), 0)
        #     pygame.draw.polygon(self.background, GREEN, [(x - 25, y), (x + 25, y), (x, y + 50)])
        #
        # pygame.display.update()

    def display_dice(self, die1, die2):
        # TODO if doubles display 4 dice
        gui_die1 = pygame.draw.rect(self.display, WHITE, (540, 420, 40, 40))
        self.display.blit(pygame.font.SysFont('Arial', 25).render(str(die1), True, (0, 0, 0)), (555, 435))
        gui_die2 = pygame.draw.rect(self.display, WHITE, (600, 420, 40, 40))
        self.display.blit(pygame.font.SysFont('Arial', 25).render(str(die2), True, (0, 0, 0)), (615, 435))
        pygame.display.update([gui_die1, gui_die2])

    def clear_dice(self):
        rect1 = self.display.blit(self.background, (540, 420), [540, 420, 40, 40])
        rect2 = self.display.blit(self.background, (600, 420), [600, 420, 40, 40])
        pygame.display.update([rect1, rect2])

    def display_pieces(self):
        for piece in self.board.get_pieces():
            location = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0], self.board))
            pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, 25)
        pygame.display.flip()

    def update_piece(self, piece, old_loc):
        location = self.pos_to_screen(old_loc, self.calculate_spacing(old_loc[0], self.board))
        self.display.blit(self.background, (location[0] - 25, location[1] - 25),
                          [location[0] - 25, location[1] - 25, 50, 50])

        location = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0], self.board))
        pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, 25)
        # TODO dont flip
        pygame.display.flip()

    def display_turn(self, turn):
        self.display.blit(self.background, (562, 8), [558, 4, 100, 14])
        turn = 'White\'s Go' if turn == 'w' else 'Black\'s Go'
        display_turn = pygame.font.SysFont('Arial', 25).render(turn, True, (0, 0, 0))
        rect = self.display.blit(display_turn, (562, 8))
        pygame.display.update([rect])

    def run(self):
        running = True
        while self.playing and running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # TODO encode into the state the source and only store thr last click.
                    # I.E. if the state is selected and then another click is fired assume this
                    # click is the destination. Therefore the source click location need to be saved
                    # in the 'selected' state object

                    index = self.screen_to_pos(event)
                    if event.button == 1 and self.dice_rolled(event):
                        self.action = Action.roll

                    elif event.button == 1 and self.piece_selected(index, event):
                        self.action = Action.select
                        self.extras['source'] = self.screen_to_pos(event)

                    elif event.button == 1 and not self.piece_selected(index, event):
                        self.action = Action.move
                        if 'source' in self.extras:
                            self.extras['destination'] = self.screen_to_pos(event)

                if event.type == pygame.QUIT:
                    running = False

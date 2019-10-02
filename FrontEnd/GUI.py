import enum
import math

import pygame, random, time
from pygame import font

WHITE = (255, 255, 255)
WOOD = (200, 200, 150)
BLACK = (0, 0, 0)


class GUI:

    def __init__(self, game):
        res = (1200, 824)
        self.game = game
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(res)
        self.background = pygame.transform.smoothscale(pygame.image.load('./backgammon/Assets/board.png').convert(),
                                                       res)

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

    def calculate_spacing(self, x):
        if len(self.game.board.pieces[x]) <= 5:
            return 50
        else:
            return int(round(50 - (len(self.game.board.pieces[x]) * 1.5)))

    def piece_selected(self, x, event):
        if x is None:
            return False
        else:
            dis = self.calculate_spacing(x)
            if x > 11 and event.pos[1] < 410:
                return (dis * len(self.game.board.pieces[x]) - 25) <= event.pos[1] <= (
                        dis * len(self.game.board.pieces[x]) + 25)
            else:
                return (790 - (dis * len(self.game.board.pieces[x]))) <= event.pos[1] <= (
                        840 - (dis * len(self.game.board.pieces[x])))

    def display_dice(self, die1, die2):
        pygame.draw.rect(self.display, WHITE, (540, 420, 40, 40))
        self.display.blit(pygame.font.SysFont('Arial', 25).render(str(die1), True, (0, 0, 0)), (555, 435))
        pygame.draw.rect(self.display, WHITE, (600, 420, 40, 40))
        self.display.blit(pygame.font.SysFont('Arial', 25).render(str(die2), True, (0, 0, 0)), (615, 435))
        return die1, die2

    def display_pieces(self, background):
        for piece in self.game.board.get_pieces():
            location = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0]))
            pygame.draw.circle(background, WOOD if piece.colour == 'w' else BLACK, location, 25)

    def initialise_display(self):
        pygame.init()
        self.display.blit(self.background, (0, 0))
        pygame.display.update()
        pygame.draw.rect(self.display, WHITE, (575, 790, 47, 30))
        self.display.blit(pygame.font.SysFont('Arial', 25).render('Roll', True, (0, 0, 0)), (583, 800))
        pygame.display.update()

    def clear_display(self):
        pass

    def run(self, board):
        die1, die2 = None, None
        while not self.game.game_over():
            self.clock.tick(120)
            # pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.dice_rolled(event):
                        pass
                        # die1, die2 = self.display_dice()
                    elif event.button == 1:
                        index = self.screen_to_pos(event)
                        top_piece_selected = self.piece_selected(index, event)
                        # print(str(index) + ', ' + str(top_piece_selected))
                        # if top_piece_selected and die1 is not None and die2 is not None:
                        #     print(board.get_available_moves(board.pieces[index][-1], (die1, die2)))

                if event.type == pygame.QUIT:
                    run = False

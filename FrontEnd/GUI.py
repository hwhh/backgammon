import math

import pygame, random, time
from pygame import font

WHITE = (255, 255, 255)
WOOD = (200, 200, 150)
BLACK = (0, 0, 0)


# TODO migrate this to a class?
def calculate_spacing(board, x):
    if len(board.pieces[x]) <= 5:
        return 50
    else:
        return int(round(50 - (len(board.pieces[x]) * 1.5)))


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


"""
0 -> 23
1 -> 22






11 -> 12


"""


def screen_to_pos(event, board):
    if 575 <= event.pos[0] <= 622 and 790 <= event.pos[1] <= 820:
        return "Dice Rolled"
    else:
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

        if x is not None:
            dis = calculate_spacing(board, x)
            if x <= 11 and event.pos[1] < 410:
                return (dis * len(board.pieces[x]) - 25) <= event.pos[1] <= (dis * len(board.pieces[x]) + 25), x
            else:
                return (790 - (dis * len(board.pieces[x]))) <= event.pos[1] <= (840 - (dis * len(board.pieces[x]))), x


def roll_dice(display):
    die1, die2 = random.choice([1, 2, 3, 4, 5, 6]), random.choice([1, 2, 3, 4, 5, 6])
    font = pygame.font.SysFont('Arial', 25)
    pygame.draw.rect(display, WHITE, (540, 420, 40, 40))
    display.blit(font.render(str(die1), True, (0, 0, 0)), (555, 435))
    pygame.draw.rect(display, WHITE, (600, 420, 40, 40))
    display.blit(font.render(str(die2), True, (0, 0, 0)), (615, 435))
    return die1, die2


def run_game(board):
    pygame.init()
    res = (1200, 824)
    display = pygame.display.set_mode(res)

    background = pygame.transform.smoothscale(pygame.image.load('./Assets/board.png').convert(), res)

    for piece in board.get_pieces():
        location = pos_to_screen(piece.loc, calculate_spacing(board, piece.loc[0]))
        pygame.draw.circle(background, WOOD if piece.colour == 'w' else BLACK, location, 25)
    clock = pygame.time.Clock()
    display.blit(background, (0, 0))
    pygame.display.update()

    font = pygame.font.SysFont('Arial', 25)
    pygame.draw.rect(display, WHITE, (575, 790, 47, 30))
    display.blit(font.render('Roll', True, (0, 0, 0)), (583, 800))
    pygame.display.update()

    run = True  # todo get the game state
    die1, die2 = None, None
    while run:
        clock.tick(120)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    index = screen_to_pos(event, board)
                    print(str(event.pos[0]) + ", " + str(event.pos[1]))
                    print(index)
                    if index == "Dice Rolled":
                        die1, die2 = roll_dice(display)

                    elif die1 is not None and die2 is not None and index[0]:
                        print(board.get_available_moves(board.pieces[index[1]][-1], (die1, die2)))

            if event.type == pygame.QUIT:
                run = False

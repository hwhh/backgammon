import math

import pygame

WHITE = (200, 200, 150)
BLACK = (0, 0, 0)


# TODO only 10 rows supported atm screen_to_pos not working

# 6 is the max -> up to 15 but then stack?


def draw_counters(board):
    for piece in board.pieces:  # TODO rename pieces to spikes or something better
        continue


def pos_to_screen(board_location, distance):  # TODO add max y limits for counters
    if board_location[0] < 6:
        return (-15 + (90 * (board_location[0] + 1))), (distance * (board_location[1] + 1))
    elif 6 <= board_location[0] < 12:
        return (45 + (90 * (board_location[0] + 1))), (distance * (board_location[1] + 1))
    elif 12 <= board_location[0] < 17:
        return (-15 + (90 * (board_location[0] - 11))), (765 - (distance * (board_location[1])))
    elif board_location[0] > 17:
        return (45 + (90 * (board_location[0] - 11))), (765 - (distance * (board_location[1])))


def screen_to_pos(event):
    if event.pos[0] < 575 and event.pos[1] > 410:
        return math.floor((event.pos[0] / 90)) + 12
    elif event.pos[0] < 575 and event.pos[1] <= 410:
        return math.floor((event.pos[0] / 90))
    elif event.pos[0] >= 575 and event.pos[1] > 410:
        return math.floor(((event.pos[0] - 80) / 90)) + 12
    elif event.pos[0] >= 575 and event.pos[1] <= 410:
        return math.floor(((event.pos[0] - 80) / 90))




def run_game(board):
    pygame.init()
    res = (1200, 824)
    display = pygame.display.set_mode(res)

    background = pygame.transform.smoothscale(pygame.image.load('./backgammon/Assets/board.png').convert(), res)

    counters = []
    for piece in board.get_pieces():
        if len(board.pieces[piece.loc[0]]) <= 5:
            distance = 50
        else:
            distance = int(round(50 - (len(board.pieces[piece.loc[0]]) * 1.5)))
        pygame.draw.circle(background, WHITE if piece.colour == 'w' else BLACK, pos_to_screen(piece.loc, distance), 25)

    #

    # for i in range(15):
    #     pygame.draw.circle(background, BLACK, pos_to_screen((3, i)), 30)
    #
    # a = 0
    # clock = pygame.time.Clock()

    # display.blit(background, (0, 0))
    # pygame.display.update()
    # while True:
    #     clock.tick(60)
    #     rect = (a, 8, 339, 205)
    #     display.blit(background, rect, rect)  # draw the needed part of the background
    #     pygame.display.update(rect)  # update the changed area
    #     a += 10
    #     rect = (a, 8, 339, 205)
    #     pygame.draw.rect(display, (255, 0, 0), rect)
    #     pygame.display.update(rect)  # update the changed area

    clock = pygame.time.Clock()

    display.blit(background, (0, 0))
    pygame.display.update()

    run = True  # todo get the game state
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    index = screen_to_pos(event)
                    print(index)
                    # print(board.move((x, y), None))
            if event.type == pygame.QUIT:
                run = False

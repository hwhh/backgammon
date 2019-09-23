import math

import pygame

WHITE = (200, 200, 150)
BLACK = (0, 0, 0)


# TODO only 10 rows supported atm screen_to_pos not working


def pos_to_screen(board_location):
    if board_location[0] < 6:
        x = -15 + (90 * (board_location[0] + 1))
    else:
        x = 45 + (90 * (board_location[0] + 1))

    if board_location[1] < 5:
        y = 61 * (board_location[1] + 1)
    else:
        y = 155 + (61 * (board_location[1] + 1))
    return x, y


def screen_to_pos(event):
    if event.pos[0] < 575:
        x = math.floor((event.pos[0] / 90))
    else:
        x = math.floor(((event.pos[0] - 80) / 90))
    if event.pos[1] > 410:
        y = math.floor((event.pos[1] - 150) / 65)
    else:
        y = math.floor((event.pos[1] - 30) / 65)
    return x, y


def run_game(board):
    pygame.init()
    res = (1200, 824)
    display = pygame.display.set_mode(res)

    background = pygame.transform.smoothscale(pygame.image.load('./backgammon/Assets/board.png').convert(), res)

    counters = []
    for piece in board.get_pieces():
        if piece.colour == 'w':
            pygame.draw.circle(background, WHITE, pos_to_screen(piece.loc), 30)
        else:
            pygame.draw.circle(background, BLACK, pos_to_screen(piece.loc), 30)

    a = 0
    clock = pygame.time.Clock()

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
                    x, y = screen_to_pos(event)
                    print(x, y)
                    print(board.move((x, y), None))
            if event.type == pygame.QUIT:
                run = False

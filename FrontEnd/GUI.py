import pygame

WHITE = (200, 200, 150)
BLACK = (0, 0, 0)

"""
  90 pixels between spikes
  80 x 355 = spike
  50, 30 = top corner

  top half = start 45 x 30
  bottom half =  start + 60
  second half = start + 50 (bar)


  radius = 25 pixels

  0, 0 -> 70, 55


"""


def pos_to_screen(board_location):
    if board_location[1] < 6:
        x = -15 + (90 * (board_location[1] + 1))
    else:
        x = 45 + (90 * (board_location[1] + 1))

    if board_location[0] < 5:
        y = 0 + (61 * (board_location[0] + 1))
    else:
        y = 155 + (61 * (board_location[0] + 1))

    return x, y


def screen_to_pos():
    pass


def run_game(pieces):
    pygame.init()
    res = (1200, 824)
    display = pygame.display.set_mode(res)

    background = pygame.transform.smoothscale(pygame.image.load('./backgammon/Assets/board.png').convert(), res)

    for piece in pieces:
        if piece.colour == 'w':
            pygame.draw.circle(background, WHITE, pos_to_screen(piece.board_location), 30)
        else:
            pygame.draw.circle(background, BLACK, pos_to_screen(piece.board_location), 30)

    clock = pygame.time.Clock()

    display.blit(background, (0, 0))
    pygame.display.update()

    run = True  # todo get the game state
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event)
            if event.type == pygame.QUIT:
                run = False

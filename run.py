import pygame

pygame.init()
res = (1200, 824)
display = pygame.display.set_mode(res, pygame.RESIZABLE)

background = pygame.transform.smoothscale(pygame.image.load(r'./backgammon/Assets/board.png').convert(), res)
a = 0
clock = pygame.time.Clock()

display.blit(background, (0, 0))
pygame.display.update()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("You pressed the left mouse button")

















    # rect = (a, 8, 339, 205)
    # display.blit(background, rect, rect)  # draw the needed part of the background
    # pygame.display.update(rect)  # update the changed area
    # a += 10
    # rect = (a, 8, 339, 205)
    # pygame.draw.rect(display, (255, 0, 0), rect)
    # pygame.display.update(rect)  # update the changed area

# e
#
# # initialize game engine
# pygame.init()
#
# clock_tick_rate = 2
#
# screen = pygame.display.set_mode((1200, 824))
#
# dead = False
# clock = pygame.time.Clock()
#
#
# background_image = pygame.image.load('./backgammon/Assets/board.png').convert()
#
# while dead == False:
#
#     # if pygame.mouse.get_pressed()[0]:
#     #     coords = pygame.mouse.get_pos()
#     #     print(coords)
#
#     for event in pygame.event.get():
#
#         # print(event)
#
# if event.type == pygame.MOUSEBUTTONDOWN:
#     if event.button == 1:
#         print("You pressed the left mouse button")
#
#         if event.type == pygame.QUIT:
#             dead = True
#
#     screen.blit(background_image, [0, 0])
#
#     pygame.display.flip()
#     # clock.tick(clock_tick_rate)

import pygame

# initialize game engine
pygame.init()

animation_increment = 10
clock_tick_rate = 20

screen = pygame.display.set_mode((1200, 824))

dead = False
clock = pygame.time.Clock()
background_image = pygame.image.load('./Assets/board.png').convert()

while dead == False:

    if pygame.mouse.get_pressed()[0]:
        coords = pygame.mouse.get_pos()
        print(coords)

    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            dead = True

    screen.blit(background_image, [0, 0])

    pygame.display.flip()
    clock.tick(clock_tick_rate)

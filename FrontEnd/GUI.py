import pygame

from BackEnd.Utilities.Action import Action, ActionType

WHITE = (255, 255, 255)
WOOD = (200, 200, 150)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50, 50)

FONT_SIZE = 25
CIRCLE_RAD = 25  # TODO get rid of magic numbers
CIRCLE_DIAM = CIRCLE_RAD * 2
BOARDER_WIDTH = 28
HOME_WIDTH = 111
BAR_WIDTH = 53
SPIKE_WIDTH = 90
BOARD_WIDTH = 1280
BOARD_HEIGHT = 824
TRIANGLE_HEIGHT = 300
TRIANGLE_WIDTH = 70
TRIANGLE_OUTLINE = 3
RIGHT_HALF = BOARD_WIDTH - (HOME_WIDTH + CIRCLE_DIAM)
LEFT_HALF = BOARD_WIDTH - (HOME_WIDTH + CIRCLE_DIAM + BAR_WIDTH)
QUAD_1 = 5
QUAD_2 = 11
QUAD_3 = 17
QUAD_4 = 23

DICE_WIDTH = 40
DICE_HEIGHT = DICE_WIDTH

ROLL_BUTTON_WIDTH = ""
ROLL_BUTTON_HEIGHT = ""


# TODO remove more magic numbers
class GUI:

    def __init__(self):
        pygame.init()
        res = (BOARD_WIDTH, BOARD_HEIGHT)
        self.turn = None
        self.selected_piece = None
        self.available_moves = None
        self.board = None
        self.action = None
        self.playing = True
        self.extras = {}
        self.clock = pygame.time.Clock()
        self.players = []
        self.display = pygame.display.set_mode(res)
        self.background = pygame.transform.smoothscale(pygame.image.load('./Assets/board.png').convert(), res)
        rect1 = self.display.blit(self.background, (0, 0))

        rect2 = pygame.draw.rect(self.display, WHITE, (575, 795, 47, 25))
        rect3 = self.display.blit(pygame.font.SysFont('Arial', FONT_SIZE).render('Roll', True, (0, 0, 0)), (583, 800))

        pygame.display.update([rect1, rect2, rect3])

    @staticmethod
    def pos_to_screen(board_location, distance):
        if board_location[0] <= QUAD_1:  # In first quadrant

            x = abs((board_location[0] * SPIKE_WIDTH) - RIGHT_HALF)
            y = (BOARD_HEIGHT - (BOARDER_WIDTH + CIRCLE_RAD) - (distance * (board_location[1])))

        elif QUAD_1 < board_location[0] <= QUAD_2:  # In second quadrant
            x = abs((board_location[0] * SPIKE_WIDTH) - LEFT_HALF)
            y = (BOARD_HEIGHT - (BOARDER_WIDTH + CIRCLE_RAD) - (distance * (board_location[1])))

        elif QUAD_2 < board_location[0] <= QUAD_3:  # In third quadrant
            x = abs((abs(board_location[0] - 23) * SPIKE_WIDTH) - LEFT_HALF)
            y = ((CIRCLE_RAD + BOARDER_WIDTH) + (distance * (board_location[1])))

        else:  # In fourth quadrant
            x = abs((abs(board_location[0] - 23) * SPIKE_WIDTH) - RIGHT_HALF)
            y = ((CIRCLE_RAD + BOARDER_WIDTH) + (distance * (board_location[1])))

        # TODO draw number of counters stacked at this point
        # TODO fix bug with distance shifting the counter off the edge of board

        if board_location[0] <= 11 and y < (BOARD_HEIGHT / 2) + CIRCLE_RAD:
            y = (BOARD_HEIGHT / 2) + CIRCLE_RAD
        if board_location[0] > 11 and y > (BOARD_HEIGHT / 2) - CIRCLE_RAD:
            y = (BOARD_HEIGHT / 2) - CIRCLE_RAD
        return x, y

    @staticmethod
    def screen_to_pos(event):
        x = None
        for i in range(12):
            if i < 6 and (RIGHT_HALF - (i * SPIKE_WIDTH)) - CIRCLE_DIAM <= event.pos[0] <= (
                    RIGHT_HALF - (i * SPIKE_WIDTH)) + CIRCLE_DIAM:
                x = i
                break
            elif i >= 6 and (LEFT_HALF - (i * SPIKE_WIDTH)) - CIRCLE_DIAM <= event.pos[0] <= (
                    LEFT_HALF - (i * SPIKE_WIDTH)) + CIRCLE_DIAM:
                x = i
                break
        if event.pos[1] <= (BOARD_HEIGHT / 2) and x is not None:
            x = 23 - x
        return x

    @staticmethod
    def dice_rolled(event):
        return 575 <= event.pos[0] <= 622 and 790 <= event.pos[1] <= 820

    def calculate_spacing(self, x):
        # TODO if the row exceeds 8, reblit entire row with smaller spacing
        # TODO if the piece is captured or bared off. x

        if len(self.board.pieces[x]) <= 7:

            return 50
        else:
            return int(round(CIRCLE_DIAM - (len(self.board.pieces[x]) * 1.5)))

    def get_action(self):
        action = self.action
        self.action = None
        return action

    def get_extras(self):
        return self.extras

    def clear_extras(self):
        self.extras = {}

    def set_board(self, board):
        self.board = board

    def set_playing(self, playing):
        self.playing = playing

    def set_players(self, players):
        self.players = players

    def piece_selected(self, x, event):
        if x is None:
            return False
        else:
            dis = self.calculate_spacing(x)
            if x > 11 and event.pos[1] < 410:
                return (dis * len(self.board.pieces[x]) - CIRCLE_RAD) <= event.pos[1] <= (
                        dis * len(self.board.pieces[x]) + CIRCLE_RAD)
            else:
                return (790 - (dis * len(self.board.pieces[x]))) <= event.pos[1] <= (
                        840 - (dis * len(self.board.pieces[x])))

    def remove_highlight_moves(self):
        if self.available_moves is not None:
            for move in self.available_moves:
                self.update_row(move)
        pygame.display.flip()

    def display_dice(self, die1, die2):
        # TODO if doubles display 4 dice
        gui_die1 = pygame.draw.rect(self.display, WHITE, (540, 420, DICE_WIDTH, DICE_HEIGHT))
        self.display.blit(pygame.font.SysFont('Arial', FONT_SIZE).render(str(die1), True, (0, 0, 0)), (555, 435))
        gui_die2 = pygame.draw.rect(self.display, WHITE, (600, 420, DICE_WIDTH, DICE_HEIGHT))
        self.display.blit(pygame.font.SysFont('Arial', FONT_SIZE).render(str(die2), True, (0, 0, 0)), (615, 435))
        pygame.display.update([gui_die1, gui_die2])

    def clear_dice(self):
        rect1 = self.display.blit(self.background, (540, 420), [540, 420, DICE_WIDTH, DICE_HEIGHT])
        rect2 = self.display.blit(self.background, (600, 420), [600, 420, DICE_WIDTH, DICE_HEIGHT])
        pygame.display.update([rect1, rect2])

    def highlight_piece(self, piece):
        self.selected_piece = piece
        # Remove old piece
        loc = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0]))
        self.display.blit(self.background, (loc[0] - CIRCLE_RAD, loc[1] - CIRCLE_RAD),
                          [loc[0] - CIRCLE_RAD, loc[1] - CIRCLE_RAD, CIRCLE_DIAM, CIRCLE_DIAM])
        # Display new Piece
        loc = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0]))
        pygame.draw.circle(self.display, GREEN, loc, CIRCLE_RAD)
        pygame.display.flip()

    def remove_highlight_piece(self):
        if self.selected_piece is not None:
            # Remove old piece
            loc = self.pos_to_screen(self.selected_piece.loc,
                                     self.calculate_spacing(self.selected_piece.loc[0]))
            self.display.blit(self.background, (loc[0] - CIRCLE_RAD, loc[1] - CIRCLE_RAD),
                              [loc[0] - CIRCLE_RAD, loc[1] - CIRCLE_RAD, CIRCLE_DIAM, CIRCLE_DIAM])
            # Display new Piece
            loc = self.pos_to_screen(self.selected_piece.loc,
                                     self.calculate_spacing(self.selected_piece.loc[0]))
            pygame.draw.circle(self.display, WOOD if self.selected_piece.colour == 'w' else BLACK, loc, CIRCLE_RAD)
            self.selected_piece = None
            pygame.display.flip()

    def display_pieces(self):
        for piece in self.board.get_pieces():
            location = self.pos_to_screen(piece.loc, CIRCLE_DIAM)
            pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, CIRCLE_RAD)
        pygame.display.flip()

    def draw_captured(self, piece):
        x = (BOARD_WIDTH - (HOME_WIDTH + BOARDER_WIDTH)) // 2
        if piece.colour == 'w':
            no_captured = self.board.white_captured
            y =
        else:
            no_captured = self.board.white_captured

    def draw_completed(self):
        pass

    def update_piece(self, piece, old_loc):
        # Update old row
        if len(self.board.pieces[old_loc[0]]) >= 7:
            self.update_row(old_loc[0])
        else:
            location = self.pos_to_screen(old_loc, self.calculate_spacing(old_loc[0]))
            self.display.blit(self.background, (location[0] - CIRCLE_RAD, location[1] - CIRCLE_RAD),
                              [location[0] - CIRCLE_RAD, location[1] - CIRCLE_RAD, CIRCLE_DIAM, CIRCLE_DIAM])
        # Update new row
        if len(self.board.pieces[piece.loc[0]]) >= 7:
            self.update_row(piece.loc[0])
        else:
            location = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0]))
            pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, CIRCLE_RAD)

        pygame.display.flip()

    def update_row(self, loc):
        x, y = self.pos_to_screen((loc, 0), 0)
        if loc <= 5 or loc >= 18:  # TODO what is this ?
            x = x + 2

        distance = self.calculate_spacing(loc)
        height = max((len(self.board.pieces[loc] * distance) + CIRCLE_DIAM), (TRIANGLE_HEIGHT + 27))  # 27 = padding

        if loc <= 11:  # Bottom half
            self.display.blit(self.background,
                              (x - (TRIANGLE_WIDTH / 2) - 1,
                               y - (height - (CIRCLE_DIAM - BOARDER_WIDTH) - TRIANGLE_OUTLINE - 2)),
                              [x - (TRIANGLE_WIDTH / 2) - 1,
                               y - (height - (CIRCLE_DIAM - BOARDER_WIDTH) - TRIANGLE_OUTLINE - 2),
                               TRIANGLE_WIDTH + TRIANGLE_OUTLINE, height])
        else:  # Top half
            self.display.blit(self.background,
                              (x - (TRIANGLE_WIDTH / 2) - 1, y - (CIRCLE_DIAM - BOARDER_WIDTH) - TRIANGLE_OUTLINE - 1),
                              [x - (TRIANGLE_WIDTH / 2) - 1, y - (CIRCLE_DIAM - BOARDER_WIDTH) - TRIANGLE_OUTLINE - 1,
                               TRIANGLE_WIDTH + TRIANGLE_OUTLINE, height])

        for piece in self.board.pieces[loc]:
            location = self.pos_to_screen(piece.loc, distance)
            pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, 25)

    def highlight_moves(self, available_moves):
        self.available_moves = available_moves
        rects = []
        for move in self.available_moves:
            x, y = self.pos_to_screen((move, 0), 0)

            if move <= 5 or move >= 18:
                x = x + 2

            if move <= 11:  # Bottom half
                rect = pygame.draw.polygon(self.display, GREEN,
                                           [(x - (TRIANGLE_WIDTH / 2), y + BOARDER_WIDTH - TRIANGLE_OUTLINE),
                                            (x + (TRIANGLE_WIDTH / 2), y + BOARDER_WIDTH - TRIANGLE_OUTLINE),
                                            (x, y - TRIANGLE_HEIGHT)], TRIANGLE_OUTLINE)
            else:  # Top half
                rect = pygame.draw.polygon(self.display, GREEN,
                                           [(x - (TRIANGLE_WIDTH / 2),
                                             y - (CIRCLE_DIAM - BOARDER_WIDTH + TRIANGLE_OUTLINE)),
                                            (x + (TRIANGLE_WIDTH / 2),
                                             y - (CIRCLE_DIAM - BOARDER_WIDTH + TRIANGLE_OUTLINE)),
                                            (x, y + TRIANGLE_HEIGHT)], TRIANGLE_OUTLINE)
            rects.append(rect)
        pygame.display.update(rects)

    def display_turn(self, turn):
        self.display.blit(self.background, (555, 8), [550, 4, 100, 14])
        self.turn = turn
        turn = 'White\'s Go' if turn == 'w' else 'Black\'s Go'
        display_turn = pygame.font.SysFont('Arial', FONT_SIZE).render(turn, True, (0, 0, 0))
        rect = self.display.blit(display_turn, (555, 8))
        pygame.display.update([rect])

    # THIS is only ever used for when there are players
    def run(self):
        running = True
        while self.playing and running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(str(event.pos[0]) + " " + str(event.pos[1]))
                    # Player vs Player
                    if len(self.players) == 2:
                        if self.turn == self.players[0].colour:
                            self.players[0].set_action(self.create_action(event))
                        elif self.turn == self.players[1].colour:
                            self.players[1].set_action(self.create_action(event))
                        else:  # initial roll
                            self.players[1].set_action(self.create_action(event))  # dose not matter who roles first


                    # PLayer vs AI - the human player should be player 2
                    else:
                        pass

                if event.type == pygame.QUIT:
                    self.action = ActionType.quit
                    running = False

    def create_action(self, event):
        index = self.screen_to_pos(event)
        if event.button == 1 and self.dice_rolled(event):
            return Action(ActionType.roll)

        elif event.button == 1 and self.piece_selected(index, event) and 'source' not in self.extras:
            self.extras['source'] = self.screen_to_pos(event)
            return Action(ActionType.select, self.extras)

        elif event.button == 1:
            if 'source' in self.extras:
                self.extras['destination'] = self.screen_to_pos(event)
            return Action(ActionType.move, self.extras)

import pygame

from BackEnd.Utilities.Action import Action, ActionType

WHITE = (255, 255, 255)
WOOD = (200, 200, 150)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50, 50)


# TODO after the event has taken place and board is updated hand back the board
# TODO instead of pooling create a pipe?
class GUI:

    def __init__(self):
        pygame.init()
        res = (1280, 824)
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
        rect2 = pygame.draw.rect(self.display, WHITE, (575, 790, 47, 30))
        rect3 = self.display.blit(pygame.font.SysFont('Arial', 25).render('Roll', True, (0, 0, 0)), (583, 800))
        pygame.display.update([rect1, rect2, rect3])

    @staticmethod
    def pos_to_screen(board_location, distance):

        if board_location[0] == 24 and board_location[1] == 24:
            x, y = 580, 420
        elif board_location[0] == 24 and board_location[1] == 25:
            x, y = 580, 480

        elif board_location[0] < 6:
            x, y = abs((board_location[0] * 90) - 1120), (765 - (distance * (board_location[1])))
        elif 6 <= board_location[0] < 12:
            x, y = abs((board_location[0] * 90) - 1065), (765 - (distance * (board_location[1])))
        elif 12 <= board_location[0] < 18:
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
        if event.pos[1] <= 400 and x is not None:
            x = 23 - x
        return x

    @staticmethod
    def dice_rolled(event):
        return 575 <= event.pos[0] <= 622 and 790 <= event.pos[1] <= 820

    @staticmethod
    def calculate_spacing(x, board):
        # TODO if the row exceeds 8, reblit entire row with smaller spacing

        if len(board.pieces[x]) <= 8:
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
            dis = self.calculate_spacing(x, self.board)
            if x > 11 and event.pos[1] < 410:
                return (dis * len(self.board.pieces[x]) - 25) <= event.pos[1] <= (
                        dis * len(self.board.pieces[x]) + 25)
            else:
                return (790 - (dis * len(self.board.pieces[x]))) <= event.pos[1] <= (
                        840 - (dis * len(self.board.pieces[x])))

    def highlight_moves(self, available_moves):
        self.available_moves = available_moves
        rects = []
        for move in self.available_moves:
            x, y = self.pos_to_screen((move, 0), 0)
            if move <= 5 or move >= 18:
                x = x + 2
            if move < 12:
                rect = pygame.draw.polygon(self.display, GREEN, [(x - 35, y + 25), (x + 35, y + 25), (x, y - 275)], 3)
            else:
                rect = pygame.draw.polygon(self.display, GREEN, [(x - 35, y + 25), (x + 35, y + 25), (x, y + 300)], 3)
            rects.append(rect)
        pygame.display.update(rects)

    def remove_highlight_moves(self):
        if self.available_moves is not None:
            for move in self.available_moves:
                x, y = self.pos_to_screen((move, 0), 0)
                if move <= 5 or move >= 18:
                    x = x + 2
                if move < 12:
                    self.display.blit(self.background, (x - 37, y - 280), [x - 37, y - 280, 80, 310])
                else:
                    self.display.blit(self.background, (x - 37, y + 23), [x - 37, y + 23, 80, 310])

                distance = self.calculate_spacing(move, self.board)
                for piece in self.board.pieces[move]:
                    location = self.pos_to_screen(piece.loc, )
                    pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, 25)
        pygame.display.flip()

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

    def highlight_piece(self, piece):
        self.selected_piece = piece
        loc = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0], self.board))
        self.display.blit(self.background, (loc[0] - 25, loc[1] - 25), [loc[0] - 25, loc[1] - 25, 50, 50])
        loc = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0], self.board))
        pygame.draw.circle(self.display, GREEN, loc, 25)
        pygame.display.flip()

    def remove_highlight_piece(self):
        if self.selected_piece is not None:
            loc = self.pos_to_screen(self.selected_piece.loc,
                                     self.calculate_spacing(self.selected_piece.loc[0], self.board))
            self.display.blit(self.background, (loc[0] - 25, loc[1] - 25), [loc[0] - 25, loc[1] - 25, 50, 50])
            loc = self.pos_to_screen(self.selected_piece.loc,
                                     self.calculate_spacing(self.selected_piece.loc[0], self.board))
            pygame.draw.circle(self.display, WOOD if self.selected_piece.colour == 'w' else BLACK, loc, 25)
            self.selected_piece = None
            pygame.display.flip()

    def display_pieces(self):
        for piece in self.board.get_pieces():
            location = self.pos_to_screen(piece.loc, 50)
            pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, 25)
        pygame.display.flip()

    def update_piece(self, piece, old_loc):
        distance = self.calculate_spacing(old_loc[0], self.board)

        location = self.pos_to_screen(old_loc, )

        self.display.blit(self.background, (location[0] - 25, location[1] - 25),
                          [location[0] - 25, location[1] - 25, 50, 50])

        location = self.pos_to_screen(piece.loc, self.calculate_spacing(piece.loc[0], self.board))
        pygame.draw.circle(self.display, WOOD if piece.colour == 'w' else BLACK, location, 25)
        # TODO dont flip
        pygame.display.flip()

    def update_pieces(self, row, dis, board):
        for piece in board[row]:
            pass

    def display_turn(self, turn):
        self.display.blit(self.background, (562, 8), [558, 4, 100, 14])
        self.turn = turn
        turn = 'White\'s Go' if turn == 'w' else 'Black\'s Go'
        display_turn = pygame.font.SysFont('Arial', 25).render(turn, True, (0, 0, 0))
        rect = self.display.blit(display_turn, (562, 8))
        pygame.display.update([rect])

    # THIS is only ever used for when there are players
    def run(self):
        running = True
        while self.playing and running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

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

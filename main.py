import math
import random
import sys

import numpy
import pygame

import menu


class Game:
    table = []

    def __init__(self, n, m, nr_players, ai_nr):
        if n <= 1 or m <= 1 or nr_players <= 0:
            raise Exception("The game __init__ parameters are wrong")
        self.n = n
        self.m = m
        self.table = numpy.zeros((n, m), dtype=int)
        self.nr_players = nr_players
        self.current_player = 1
        self.ai_nr = ai_nr

    def move(self, column, player_id):
        if self.current_player != player_id:
            raise Exception("Error, it isn't this players turn")
        if column >= self.m:
            raise Exception("Error, the row does not exist")
        for i in range(self.n):
            if self.table[self.n - (i + 1)][column] == 0:
                self.table[self.n - (i + 1)][column] = player_id
                break
            if i == self.n - 1:
                return "The move is invalid"
        self.current_player = (self.current_player % self.nr_players) + 1

    def get_winner(self):
        diags = [self.table[::-1, :].diagonal(i) for i in range(-self.table.shape[0] + 1, self.table.shape[1])]
        diags.extend(self.table.diagonal(i) for i in range(self.table.shape[1] - 1, -self.table.shape[0], -1))
        for i in range(self.n):
            diags.extend([self.table[i]])
        aux = numpy.rot90(self.table)
        for i in range(len(aux)):
            diags.extend([aux[i]])

        for n in diags:
            cnt = 0
            last_player = 0
            for v in n.tolist():
                if v != 0:
                    if last_player != v:
                        cnt = 0
                        last_player = v
                    cnt += 1
                    if cnt == 4:
                        return v
                else:
                    cnt = 0
                    last_player = v
        # check if the table is full
        for i in range(self.n):
            for j in range(self.m):
                if self.table[i][j] == 0:
                    return None
        return -1

    def ai_move(self, difficulty):
        if current_player < (self.nr_players - self.ai_nr) + 1:
            return False
        col = int(random.random() * self.m)
        pygame.time.wait(500)
        while self.move(col, self.current_player) is not None:
            col = int(random.random() * self.m)
        return True

    def player_move(self, column, player):
        if player < (self.nr_players - self.ai_nr) + 1:
            return self.move(column, player)
        else:
            return "It's the turn of the computer"

    def print_table(self):
        for i in range(self.n):
            print(self.table[i])


class render_game:
    def __init__(self, game):
        pygame.init()

        self.COLORS = [(0, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255)]
        self.SQUARESIZE = 100

        self.width = game.m * self.SQUARESIZE
        self.height = (game.n + 1) * self.SQUARESIZE

        size = (self.width, self.height)
        self.screen = pygame.display.set_mode(size)

    def draw_board(self):
        self.RADIUS = int(self.SQUARESIZE / 2) - 5
        self.OFFSET = int(self.SQUARESIZE / 2)
        for r in range(game.n):
            for c in range(game.m):
                pygame.draw.rect(self.screen, (0, 0, 255),
                                 (c * self.SQUARESIZE, (r + 1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                color = self.COLORS[game.table[r][c]]
                pygame.draw.circle(self.screen, color,
                                   (c * self.SQUARESIZE + self.OFFSET, (r + 1) * self.SQUARESIZE + self.OFFSET),
                                   self.RADIUS)
        pygame.display.update()

    def draw_circle_motion(self, posx, player):
        pygame.draw.rect(self.screen, self.COLORS[0], (0, 0, self.width, self.SQUARESIZE))
        pygame.draw.circle(self.screen, self.COLORS[player],
                           (int(posx / self.SQUARESIZE) * self.SQUARESIZE + self.OFFSET, self.OFFSET), self.RADIUS)
        pygame.display.update()

    def show_winner(self, winner):
        pygame.draw.rect(self.screen, self.COLORS[0], (0, 0, self.width, self.SQUARESIZE))
        myfont = pygame.font.SysFont("monospace", 50)
        if winner == -1:
            text = "It's a draw!"
            label = myfont.render(text, 1, (255, 255, 255))
        else:
            text = "Player " + str(winner) + " has won!"
            label = myfont.render(text, 1, self.COLORS[winner])
        (text_width, text_height) = myfont.size(text)

        self.screen.blit(label, ((self.width / 2) - text_width / 2, 10))
        pygame.display.update()


if __name__ == "__main__":
    ROW_COUNT, COLUMN_COUNT, nr_players, ai_nr = menu.main_menu()
    game = Game(ROW_COUNT, COLUMN_COUNT, nr_players, ai_nr)
    render = render_game(game)
    render.draw_board()
    current_player = game.current_player
    foundWinner = False
    posx = 0
    while not foundWinner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                render.draw_circle_motion(posx, current_player)
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                column = math.floor(int(posx / render.SQUARESIZE))
                ret = game.player_move(column, current_player)
                if ret is not None:
                    print(ret)
                current_player = game.current_player

                winner = game.get_winner()
                render.draw_board()
                if winner is not None:
                    foundWinner = True
                    render.show_winner(winner)
                    pygame.time.wait(5000)
                    break
                render.draw_circle_motion(posx, current_player)
        for i in range(ai_nr):
            if game.ai_move(2):
                current_player = game.current_player

                winner = game.get_winner()
                render.draw_board()
                if winner is not None:
                    foundWinner = True
                    render.show_winner(winner)
                    pygame.time.wait(3000)
                    break
                render.draw_circle_motion(posx, current_player)

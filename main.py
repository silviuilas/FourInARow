import math
import sys

import numpy
import pygame

import menu


class Game:
    table = []

    def __init__(self, n, m, nr_players):
        if n <= 1 or m <= 1 or nr_players <= 0:
            raise Exception("The game __init__ parameters are wrong")
        self.n = n
        self.m = m
        self.table = numpy.zeros((n, m), dtype=int)
        self.nr_players = nr_players
        self.current_player = 1

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
        return None

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
        myfont = pygame.font.SysFont("monospace", 60)
        text = "Player " + str(winner) + " has won!"
        (text_width, text_height) = myfont.size(text)
        label = myfont.render(text, 1, self.COLORS[winner])
        self.screen.blit(label, ((self.width / 2) - text_width / 2, 10))
        pygame.display.update()


if __name__ == "__main__":
    ROW_COUNT, COLUMN_COUNT, nr_players, ai_nr = menu.main_menu()
    game = Game(ROW_COUNT, COLUMN_COUNT, nr_players)
    render = render_game(game)
    render.draw_board()
    current_player = 1
    foundWinner = False
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
                ret = game.move(column, current_player)
                if ret is None:
                    current_player = (current_player % nr_players) + 1
                else:
                    print(ret)
                render.draw_board()
                winner = game.get_winner()
                if winner is not None:
                    foundWinner = True
                    render.show_winner(winner)
                    pygame.time.wait(3000)
                    break
                render.draw_circle_motion(posx, current_player)

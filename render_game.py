import pygame


class RenderGame:
    def __init__(self, n, m):
        pygame.init()

        self.COLORS = [(0, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255)]
        self.SQUARESIZE = 100

        self.n = n
        self.m = m
        self.width = self.m * self.SQUARESIZE
        self.height = (self.n + 1) * self.SQUARESIZE

        size = (self.width, self.height)
        self.screen = pygame.display.set_mode(size)

    def draw_board(self, game):
        self.RADIUS = int(self.SQUARESIZE / 2) - 5
        self.OFFSET = int(self.SQUARESIZE / 2)
        for r in range(self.n):
            for c in range(self.m):
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

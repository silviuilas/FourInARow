import math
import random
import sys

import pygame


class Player:
    def __init__(self, game, name):
        self.game = game
        self.name = name

    def move(self, column):
        return self.game.move(column, self.name)


class Human(Player):
    def __init__(self, game, name, render):
        super().__init__(game, name)
        self.render = render

    def make_move(self):
        render = self.render
        found_move = False
        while not found_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    render.draw_circle_motion(posx, self.name)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    column = math.floor(int(posx / render.SQUARESIZE))
                    ret = self.move(column)
                    if ret is not None:
                        print(ret)
                    else:
                        render.draw_circle_motion(posx, self.game.current_player)
                        found_move = True


class AI(Player):
    def __init__(self, game, name, level):
        super().__init__(game, name)
        self.level = level

    def make_move(self):
        col = int(random.random() * self.game.m)
        while self.move(col) is not None:
            col = int(random.random() * self.game.m)
        return True

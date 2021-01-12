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

    def get_score(self):
        # Calculates the score of the player in relationship with other players and returns it.
        current_score = 0
        for n in self.game.transform_table():
            cnt = 0
            last_player = 0
            if len(n) >= 4:
                for v in n.tolist():
                    if v != 0:
                        if last_player != v:
                            cnt = 0
                            last_player = v
                        cnt += 1
                        if last_player == self.name:
                            current_score += pow(cnt, 2)
                        else:
                            current_score -= pow(cnt, 3)
                        if cnt == 4:
                            if last_player == self.name:
                                return 999999999
                            else:
                                return -999999999
                    else:
                        cnt = 0
                        last_player = v
        return current_score


class Human(Player):
    def __init__(self, game, name, render):
        super().__init__(game, name)
        self.render = render

    def make_move(self):
        """
            Using the ui, the human player selects a move and makes it directly on the game.
            :return Nothing
        """
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

    # The AI makes a move based on it's level
    def make_move(self):
        """
            The AI makes a move based on it's level
            :return Nothing
        """
        if self.level == 0:
            col = int(random.random() * self.game.m)
        else:
            aux = self.level
            if self.level == 3:
                aux += 2
            col = self.min_max(aux, 0)
        while self.move(col) is not None:
            col = int(random.random() * self.game.m)

    def min_max(self, max_depth, current_depth):
        """
            The min max algorithm that selects a move
            :param max_depth: The maximum depth that the min_max algorithm can get to
            :param current_depth: The current depth of the algorithm
            :return res: The selected move

        """
        mvs = self.game.generate_possible_moves()
        if self.game.remaining_spots == 0 or current_depth == max_depth or len(mvs) == 0:
            return self.get_score()

        # Vec holds the scores from each possible move
        vec = []
        for mv in mvs:
            current_player = self.game.current_player
            self.game.move(mv, current_player)
            ras = self.min_max(max_depth, current_depth + 1)
            self.game.undo_move(mv, current_player)
            vec.append(ras)

        maxi = -9999999
        maxi_i = -1
        mini = 9999999
        mini_i = -1
        # Get the min and max index from the list
        for i in range(len(vec)):
            if vec[i] >= maxi:
                maxi = vec[i]
                maxi_i = i
            if vec[i] <= mini:
                mini = vec[i]
                mini_i = i
        # If we are not in root we return min or max
        if current_depth != 0:
            if current_depth % 2 == 0:
                return vec[maxi_i]
            else:
                return vec[mini_i]
        else:
            return maxi_i

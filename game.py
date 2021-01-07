import numpy
import pygame


class Game:
    table = []

    def __init__(self, n, m):
        if n <= 1 or m <= 1:
            raise Exception("The game __init__ parameters are wrong")
        self.n = n
        self.m = m
        self.table = numpy.zeros((n, m), dtype=int)
        self.nr_players = 0
        self.players = []
        self.current_player = 1
        self.remaining_spots = n * m

    def add_player(self, player):
        self.players.append(player)
        self.nr_players = len(self.players)

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
        self.remaining_spots -= 1

    def undo_move(self, column, player_id):
        for i in range(self.n):
            if self.table[i][column] == player_id:
                self.table[i][column] = 0
                break
            elif self.table[i][column] != 0:
                raise Exception("Something is wrong, the undo can't take place now")
            if i == self.n - 1:
                raise Exception("The undo move is invalid")
        self.current_player -= 1
        if self.current_player == 0:
            self.current_player = self.nr_players
        self.remaining_spots += 1

    def generate_possible_moves(self):
        mvs = []
        for i in range(self.m):
            if self.table[0][i] == 0:
                mvs.append(i)
        return mvs

    def transform_table(self):
        diags = [self.table[::-1, :].diagonal(i) for i in range(-self.table.shape[0] + 1, self.table.shape[1])]
        diags.extend(self.table.diagonal(i) for i in range(self.table.shape[1] - 1, -self.table.shape[0], -1))
        for i in range(self.n):
            diags.extend([self.table[i]])
        aux = numpy.rot90(self.table)
        for i in range(len(aux)):
            diags.extend([aux[i]])
        return diags

    def get_winner(self):
        trns = self.transform_table()
        for n in trns:
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
        if self.remaining_spots != 0:
            return None
        return -1

    def start_game(self, render):
        found_winner = False
        render.draw_board(self)
        while not found_winner:
            for x in self.players:
                x.make_move()
                render.draw_board(self)
                winner = self.get_winner()
                if winner is not None:
                    found_winner = True
                    render.show_winner(winner)
                    pygame.time.wait(5000)
                    break
        self.table = numpy.zeros((self.n, self.m), dtype=int)
        self.current_player = 1

    def print_table(self):
        for i in range(self.n):
            print(self.table[i])

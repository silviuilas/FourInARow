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
        """
           Add a player to the current game
           :param player: An object of class Player
           :return: Nothing.
        """
        self.players.append(player)
        self.nr_players = len(self.players)

    def move(self, column, player_id):
        """
            Validate and make a player move if possible
           :param column: The number of the column
           :param player_id: the id of the column
           :return: If successful returns nothing and if the move
                    is not valid returns a string with the error
        """
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
        """
            Undo a specific move. Warning. It doesn't check that it's the last move.
            :param column: The number of the column
            :param player_id: the id of the column
            :return Nothing.
        """
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
        # Returns a list of the remaining possible moves.

        mvs = []
        for i in range(self.m):
            if self.table[0][i] == 0:
                mvs.append(i)
        return mvs

    def transform_table(self):
        # Transforms the table in a way that it is easy to check how many pieces in a row there are
        # Make a list of lists that contains all the diagonals
        list_of_lists = [self.table[::-1, :].diagonal(i) for i in range(-self.table.shape[0] + 1, self.table.shape[1])]
        list_of_lists.extend(self.table.diagonal(i) for i in range(self.table.shape[1] - 1, -self.table.shape[0], -1))
        # Extend that list so it has all the rows
        for i in range(self.n):
            list_of_lists.extend([self.table[i]])
        # Further extend it to have all the columns
        aux = numpy.rot90(self.table)
        for i in range(len(aux)):
            list_of_lists.extend([aux[i]])
        return list_of_lists

    def get_winner(self):
        # Returns the winner of the game
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
        """
            Starts the game and waits for the game to finish
            :param render: An object of type RenderGame that is the player point of view
            :return : Nothing.
        """
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
        # Shows the table on the screen
        for i in range(self.n):
            print(self.table[i])

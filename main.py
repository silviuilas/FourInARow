import numpy


class Game:
    table = []

    def __init__(self, n, m, nr_players):
        if n <= 1 or m <= 1 or nr_players <= 1:
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
            counter = numpy.zeros(self.nr_players, dtype=int)
            for v in n.tolist():
                if v != 0:
                    counter[v - 1] = counter[v - 1] + 1
                    if counter[v - 1] == 4:
                        return v
        return None

    def print_table(self):
        for i in range(self.n):
            print(self.table[i])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    n = int(input("Define length of the matrix: "))
    m = int(input("Define width of the matrix: "))
    nr_players = int(input("Define the number of players: "))
    game = Game(n, m, nr_players)

    current_player = 1
    while True:
        column = int(input("Select the column: "))
        ret = game.move(column, current_player)
        if ret is None:
            current_player = (current_player % nr_players) + 1
            game.print_table()
        else:
            print(ret)
        winner = game.get_winner()
        if winner is not None:
            print("The winner is player " + str(winner))
            break

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

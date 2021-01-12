import sys

import game
import menu
import player
import render_game as rg

if __name__ == "__main__":

    # Take the arguments from the system
    if len(sys.argv[1:]) is not 0:
        args = sys.argv[1:-1].copy()
        human_player_first = True if sys.argv[-1] == 1 else False
        for i in range(0, len(args)):
            args[i] = int(args[i])
        ROW_COUNT, COLUMN_COUNT, nr_players, ai_nr, ai_level = args
    else:  # Take the arguments from the UI
        human_player_first = True
        ROW_COUNT, COLUMN_COUNT, nr_players, ai_nr, ai_level = menu.main_menu()
    render = rg.RenderGame(ROW_COUNT, COLUMN_COUNT)
    game = game.Game(ROW_COUNT, COLUMN_COUNT)

    if human_player_first:
        for i in range(nr_players - ai_nr):
            game.add_player(player.Human(game, i + 1, render))
        for i in range(nr_players - ai_nr, nr_players):
            game.add_player(player.AI(game, i + 1, ai_level))
    else:
        for i in range(nr_players - ai_nr):
            game.add_player(player.AI(game, i + 1, ai_level))
        for i in range(nr_players - ai_nr, nr_players):
            game.add_player(player.Human(game, i + 1, render))

    render.draw_board(game)
    game.start_game(render)

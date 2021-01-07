import threading

import game
import menu
import player
import render_game as rg


if __name__ == "__main__":
    ROW_COUNT, COLUMN_COUNT, nr_players, ai_nr, ai_level = menu.main_menu()
    render = rg.RenderGame(ROW_COUNT, COLUMN_COUNT)
    game = game.Game(ROW_COUNT, COLUMN_COUNT)

    for i in range(nr_players - ai_nr):
        game.add_player(player.Human(game, i + 1, render))
    for i in range(nr_players - ai_nr, nr_players):
        game.add_player(player.AI(game, i + 1, ai_level))

    render.draw_board(game)
    game.start_game(render)

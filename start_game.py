from word_finder import *
from game import *

board = Board()
# board = Board(dim=5, csv_file="big_board.csv")
board.populate()

player_list = []
game = Game(player_list, board)
player = Player(game, 0)
game.player_list.append(player)
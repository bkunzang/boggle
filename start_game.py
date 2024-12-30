from word_finder import *
from game import *

board = Board()
board.populate()

player_list = []
game = Game(player_list, board)
player = Player(game, 0)
game.player_list.append(player)
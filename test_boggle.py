from word_finder import *
from game import *
import random
import pytest

def get_test_board():
    random.seed(58)
    test_board = Board()
    test_board.populate()
    return test_board

test_board = get_test_board()
test_words = ['gnu', 'gnus', 'gnat', 'gnats', 'gan', 'gat', 'gats', 'aunt', 'aunts', 'anus', 'ant',
            'ants', 'anta', 'ana', 'anatto', 'anattos', 'anga', 'aqua', 'aah', 'att', 'oms', 'our', 
            'oust', 'out', 'outs', 'mol', 'mols', 'mount', 'mounts', 'mouth', 'mouths', 'mos', 'most', 
            'mot', 'mots', 'mott', 'motts', 'moth', 'moths', 'rhus', 'rust', 'rush', 'ruana', 'run', 'runs', 
            'runt', 'runts', 'rung', 'rut', 'ruts', 'ruth', 'ruths', 'uns', 'uts', 'uta', 'nurl', 'nurls', 
            'nus', 'nut', 'nuts', 'nah', 'nth', 'nag', 'hurl', 'hurls', 'hush', 'hun', 'huns', 'hunt', 'hunts', 
            'hung', 'hut', 'huts', 'haul', 'hauls', 'haunt', 'haunts', 'haut', 'hansom', 'hant', 'hants', 
            'hang', 'tush', 'tun', 'tuns', 'tuna', 'tung', 'tan', 'tans', 'tang', 'tag', 'tolu', 'tolus', 
            'tom', 'toms', 'tour', 'tout', 'touts', 'tost', 'tosh', 'lour', 'lout', 'louts', 'lost', 'lot', 
            'lots', 'loth', 'lust', 'lush', 'luna', 'lunt', 'lunts', 'lung', 'slot', 'sloth', 'slur', 'slung',
            'slut', 'sol', 'sou', 'sour', 'soul', 'south', 'sot', 'soth', 'sun', 'sung', 'stour', 'stout', 
            'snath', 'snag', 'stun', 'stung', 'stang', 'stag', 'qua', 'quant', 'quants', 'quanta', 'quag']

def test_all_words():
    assert test_board.all_words == test_words

number_sampled = random.randint(1, len(test_words))
test_found = random.sample(test_words, number_sampled)
test_player_list = []
test_game = Game(test_player_list, test_board)
test_player = Player(test_game, 0, test_found)
test_game.player_list.append(test_player)
def test_point_counts():
    test_player.calculate_points()
    acc = 0
    for word in test_found:
        if len(word) == 3:
            acc += 1
        elif len(word) == 4:
            acc += 1
        elif len(word) == 5:
            acc += 2
        elif len(word) == 6:
            acc += 3
        elif len(word) == 7:
            acc += 5
        else:
            acc += 11
    assert acc == test_player.point_total

    
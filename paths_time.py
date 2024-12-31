import timeit
from time import process_time
from word_finder import *
setup = board = Board()  
board.populate()

t0 = process_time()
board.old_get_words()
t1 = process_time()
board.get_words()
t2 = process_time()

x = t1 - t0
y = t2 - t1

print(x, y)
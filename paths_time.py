import timeit
from time import process_time
from word_finder import * 
t3=process_time()
board = Board(dim=5)
t4=process_time()
board.populate()
t0 = process_time()
board.get_words()
t2 = process_time()

x = t0 - t4
y = t2 - t0
z=t4-t3
print(z,x, y)
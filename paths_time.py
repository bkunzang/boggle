import timeit
from time import process_time
from word_finder import * 
t3=process_time()
board = Board()
t4=process_time()
board.populate()
t0 = process_time()
board.old_get_words()
t1 = process_time()
board.get_words()
t2 = process_time()

x = t1 - t0
y = t2 - t1
z=t4-t3
print(z,x, y)
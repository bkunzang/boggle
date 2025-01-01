import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from word_finder import *

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150


board = Board(dim=4)

def simulate():
    result = []
    for i in range(10000):
        board.populate()
        result.append(board.total_points)
        #if board.total_points >= 700:
         #   print(board, board.all_words, board.total_points)
    np_result = np.array(result)
    return np_result

def cube_change_sim():
    result = []
    for cube in board.cubes_used:
        letters_seen = set()
        for i in range(6):
            letters_seen.add(cube.letter_list[i]) 


sim = simulate()
x=stats.describe(sim)
y=sns.histplot(sim)
med=np.median(sim)
z = stats.norm.interval(0.99, loc = np.mean(sim), scale = np.std(sim) / 100)
plt.title('Distribution of Points in Big Boggle')
plt.ylabel('Frequency')
plt.xlabel('Points')
plt.show()
print(x)
print(z)
print(med)
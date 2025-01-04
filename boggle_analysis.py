import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from word_finder import *
from time import process_time
import csv

result_file = 'boggle_trials.csv'
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150


board = Board(dim=5)

def simulate():
    result = []
    words_dict = {}
    with open(result_file, 'w') as csvfile:
        writer = csv.writer(csvfile)   
        for i in range(300000):
            board.populate()
            result.append(board.total_points)
            writer.writerow([i,board.last_id, board.total_points])
            for word in board.all_words:
                if word in words_dict:
                    words_dict[word][0] += 1
                else: 
                    words_dict[word] = [1, board.last_id,i]
    np_result = np.array(result)
    return (np_result, words_dict)

def get_words():
    words_dict = {}
    board = Board(dim=5)
    with open(result_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            board.id = float(row[0])
            board.populate()
           # assert board.total_points == int(row[1])
            for word in board.all_words:
                if word in words_dict:
                    words_dict[word][0] += 1
                else:
                    words_dict[word][0] = 1
                    words_dict[word][1] = set(board.id)
    return words_dict

t1 = process_time()
result = simulate()
t2 = process_time()
sim = result[0]
words_dict = result[1]
with open('word_occurrences.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for word in words_dict:
        res = words_dict.get(word)
        writer.writerow([word, res[0], res[1], res[2]])
x=stats.describe(sim)
y=sns.histplot(sim)
med=np.median(sim)
z = stats.t.interval(0.99, 299999, loc = np.mean(sim), scale = np.std(sim) / np.sqrt(300000))
plt.title('Distribution of Points in Big Boggle')
plt.ylabel('Frequency')
plt.xlabel('Points')
plt.show()
print(x)
print(z)
print(med)
print(t2-t1)

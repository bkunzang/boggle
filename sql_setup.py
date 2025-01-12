import sqlite3
import csv

connection = sqlite3.connect("data/boggle.db")
cursor = connection.cursor()
cursor.execute('CREATE TABLE anti_suffix_trials (trial INTEGER, seed TEXT, points INTEGER)')
cursor.execute('CREATE TABLE anti_suffix_words (word TEXT, frequency INTEGER, seed TEXT, trial INTEGER)')
trials_file = 'boggle_trials_anti_suffix_cubes.csv'
words_file = 'word_occurrences_anti_suffix_cubes.csv'

with open(trials_file, 'r') as csvfile:
        to_db1 = []
        reader = csv.reader(csvfile)
        for row in reader:
                to_db1.append((int(row[0]), (row[1]), int(row[2])))


with open(words_file, 'r') as csvfile:
        to_db2 = []
        reader = csv.reader(csvfile)
        for row in reader:
                to_db2.append((row[0], int(row[1]), row[2], int(row[3])))

cursor.executemany("INSERT INTO anti_suffix_trials (trial, seed, points) VALUES (?, ?, ?);", to_db1)
cursor.executemany("INSERT INTO anti_suffix_words (word, frequency, seed, trial) VALUES (?, ?, ?, ?);", to_db2)
connection.commit()
connection.close()
            



import sqlite3
import csv

connection = sqlite3.connect("boggle.db")
cursor = connection.cursor()
cursor.execute('CREATE TABLE dictionary (word TEXT)')
#cursor.execute('CREATE TABLE old_words (word TEXT, frequency INTEGER, seed TEXT, trial INTEGER)')
#trials_file = 'boggle_trials_old_cubes.csv'
words_file = 'English_dictionary.csv'
'''
with open(trials_file, 'r') as csvfile:
        to_db1 = []
        reader = csv.reader(csvfile)
        for row in reader:
                to_db1.append((int(row[0]), (row[1]), int(row[2])))
'''

with open(words_file, 'r') as csvfile:
        to_db2 = []
        reader = csv.reader(csvfile)
        for row in reader:
                to_db2.append((row[0],))

#cursor.executemany("INSERT INTO old_trials (trial, seed, points) VALUES (?, ?, ?);", to_db1)
cursor.executemany("INSERT INTO dictionary (word) VALUES (?);", to_db2)
connection.commit()
connection.close()
            



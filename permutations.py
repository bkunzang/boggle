from word_finder import *
from cube_sets import CubeSet
import csv

cubes_file = 'English_5_standard_board.csv'

with open(cubes_file, 'r') as csvfile:
    result = ''
    reader = csv.reader(csvfile)
    for row in reader:
        result += ''.join(row)
    standard = CubeSet(result)
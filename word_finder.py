import random
import csv
import sys

csv.field_size_limit(sys.maxsize)
words_set = set()
with open('dictionary.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        words_set.add(row[0].lower())

class Board:
    def __init__(self, dim=4, csv_file="standard_board.csv"):
        '''
        A Boggle board.

        Class variables:
        - cubes_used: cubes to be used in game, loads default cube set
        - cube_configuration: properly shuffled cubes from cubes_used
        - cubes_used: cubes to be used in game, loads default cube set
        - cube_configuration: properly shuffled cubes from cubes_used
        - dim: dimension of board
        '''
        self.cubes_used = []
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                letter_list = []
                for letter in row:
                    letter_list.append(letter)
                self.cubes_used.append(Cube(letter_list))

        self.dim = dim
        self.cube_configuration = [[] for _ in range(dim)]

    def __str__(self):
        print_string = ""
        for row in self.cube_configuration:
            for elem in row:
                print_string += elem.displayed_letter + " "
            print_string += "\n"
        return print_string

    def populate(self):
        '''
        Add description here.
        '''
        # shuffle cubes in board
        map(lambda x: x.roll(), self.cubes_used)
        temp_list = list(self.cubes_used)
        while temp_list:
            for i in range(self.dim):
                for _ in range(self.dim):
                    cube = temp_list.pop(random.randint(0, len(temp_list) - 1))
                    self.cube_configuration[i].append(cube)
                    cube.roll()
        
        # add neighbors to each cube
        for row in range(self.dim):
            for col in range(self.dim):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        row_i = row + i
                        col_j = col + j
                        if row_i >= 0 and row_i < self.dim and col_j >= 0 and col_j < self.dim:
                            if i == 0 and j == 0:
                                # idk man I need to figure out how to skip this case  
                                pass
                            else:
                                self.cube_configuration[row][col].add_neighbor(self.cube_configuration[row_i][col_j])

    # get a list of paths with length in range(min,max)
    def get_paths(self, min, max):
        result = []
        for cube in self.cubes_used:
            result.extend(cube.find_paths())
        return list(filter(lambda x: len(x) >= min and len(x) < max, result))

     # get all paths of length at least 3 and then turn them into strings (i am aware that i could do this nicer with the get_paths function with minimum 4 but i haven't fixed it yet)
    def get_words(self):
        result = []
        for cube in self.cubes_used:
            for path in cube.find_paths():
                if len(path) >= 3:
                    str_path = list_to_str(path).lower()
                    if str_path in words_set:
                        result.append(str_path)
        return result

class Cube:
    '''
        A cube with letters.

        Class variables:
        - letter_list: provided list of letters, specific to each cube
        - displayed_letter: letter that will display on board after rolling
        - neighbors: Cube objects next to self
        '''
    def __init__(self, letter_list, neighbors=None):
        self.letter_list = letter_list
        self.displayed_letter = None
        self.neighbors = neighbors

    def __repr__(self):
        return self.displayed_letter

    def roll(self):
        self.displayed_letter = self.letter_list[random.randint(0, len(self.letter_list)-1)] # usually 6, but edited for testing so i don't have to add 6 faces

    def display_letter(self, letter):
        assert letter in self.letter_list
        self.displayed_letter = letter

    # adds new vertex to the neighbor sets of both at once (undirected graph)
    def add_neighbor(self, new):
        if self.neighbors is None:
            self.neighbors = []
        if new.neighbors is None:
            new.neighbors = []
        if new not in self.neighbors and self not in new.neighbors:
            self.neighbors.append(new)
            new.neighbors.append(self)
    
    def find_paths(self):
        return self.paths_helper([self])
    
    # go down and add letters to path until you can't anymore, then get rid of the last ones until you can again
    def paths_helper(self, current_path):
        result = []
        result.append(current_path[:])
        if self.neighbors is None:
            return result
        else:
            for neighbor in self.neighbors:
                if neighbor not in current_path:
                    current_path.append(neighbor)
                    newpaths = neighbor.paths_helper(current_path)
                    result.extend(newpaths)
        current_path.pop()
        return result


def list_to_str(input_list):
    result = ""
    for cube in input_list:
        result += cube.displayed_letter
    return result
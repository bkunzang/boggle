import random
import csv
import sys

class Board:
    def __init__(self, dim=4, language="English"):
        '''
        A Boggle board.

        Class variables:
        - cubes_used: cubes to be used in game, loads default cube set
        - cube_configuration: properly shuffled cubes from cubes_used
        - words_set: dictionary of all words in provided language
        - dim: dimension of board, defaults to 4x4
        - language: language of play, defaults to English
        '''
        self.cubes_used = []

        csv_file_name = language + "_standard_board.csv"
        with open(csv_file_name, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                letter_list = []
                for letter in row:
                    letter_list.append(letter)
                self.cubes_used.append(Cube(letter_list, self))

        dictionary_file_name = language + "_dictionary.csv"
        csv.field_size_limit(sys.maxsize)
        self.words_set = set()
        #self.two_prefixes_set = set()
        #self.three_prefixes_set = set()
        self.prefixes_set_list = [set() for _ in range(14)]
        with open(dictionary_file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.words_set.add(row[0].lower())
                for i in range(14):
                    if len(row[0]) >= i+2:
                        self.prefixes_set_list[i].add((row[0].lower())[:(i+2)])
                #self.two_prefixes_set.add((row[0].lower())[:2])
                #self.three_prefixes_set.add((row[0].lower())[:3])
        

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
        self.all_words = self.get_words()
    # get a list of paths with length in range(min,max)
    def get_paths(self, min, max):
        result = []
        for cube in self.cubes_used:
            result.extend(cube.find_paths())
        return list(filter(lambda x: len(x) >= min and len(x) < max, result))

     # get all paths of length at least 3 and then turn them into strings (i am aware that i could do this nicer with the get_paths function with minimum 4 but i haven't fixed it yet)
    def old_get_words(self):
        result = []
        for cube in self.cubes_used:
            for path in cube.find_paths():
                if len(path) >= 3:
                    str_path = list_to_str(path).lower()
                    if str_path in self.words_set:
                        result.append(str_path)
        return result
    
    def get_words(self):
        result = []
        for cube in self.cubes_used:
            for word in cube.find_words():
                if len(word) >= 3 and word not in result:
                    result.append(word)
        return result

class Cube:
    '''
        A cube with letters.

        Class variables:
        - letter_list: provided list of letters, specific to each cube
        - displayed_letter: letter that will display on board after rolling
        - neighbors: Cube objects next to self
        '''
    def __init__(self, letter_list, board, neighbors=None):
        self.letter_list = letter_list
        self.board = board
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
    
    def find_words(self):
        return self.words_helper([self])

    def words_helper(self, current_path):
        current_str = list_to_str(current_path).lower()
        result = []
        if current_str in self.board.words_set:
            result.append(current_str)
        if self.neighbors is None:
            return result
        if len(current_str) >= 2 and current_str not in self.board.prefixes_set_list[len(current_str)-2]:
            pass
       # elif (len(current_str) == 2 and current_str not in self.board.two_prefixes_set) or (len(current_str)==3 and current_str not in self.board.three_prefixes_set):
        #    pass
        else:
            for neighbor in self.neighbors:
                if neighbor not in current_path:
                    current_path.append(neighbor)
                    newpaths = neighbor.words_helper(current_path)
                    result.extend(newpaths)
        current_path.pop()
        return result

def list_to_str(input_list):
    result = ""
    for cube in input_list:
        result += cube.displayed_letter
    return result
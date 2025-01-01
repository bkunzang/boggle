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

        csv_file_name = language + "_" + str(dim) + "_standard_board.csv"
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
        self.prefixes_set_list = [set() for _ in range(dim*dim - 2)]
        with open(dictionary_file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.words_set.add(row[0].lower())
                for i in range(dim*dim - 2):
                    if len(row[0]) >= i+2:
                        self.prefixes_set_list[i].add((row[0].lower())[:(i+2)])
                #self.two_prefixes_set.add((row[0].lower())[:2])
                #self.three_prefixes_set.add((row[0].lower())[:3])
        

        self.dim = dim
        self.cube_configuration = [[] for _ in range(dim)]

        self.min_word_length = 3
        if dim > 4:
            self.min_word_length = 4

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
        self.cube_configuration = [[] for _ in range(self.dim)]
        map(lambda x: x.roll(), self.cubes_used)
        temp_list = list(self.cubes_used)
        while temp_list:
            for i in range(self.dim):
                for _ in range(self.dim):
                    cube = temp_list.pop(random.randint(0, len(temp_list) - 1))
                    self.cube_configuration[i].append(cube)
                    cube.clear_neighbors()
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
        self.total_points = self.get_points()
        self.num_words = len(self.all_words)

    def get_paths(self, min, max):
        '''
        Get a list of paths with length in range(min,max). Note: this method uses the obsolete find_paths() function.
        '''
        result = []
        for cube in self.cubes_used:
            result.extend(cube.find_paths())
        return list(filter(lambda x: len(x) >= min and len(x) < max, result))

    def old_get_words(self):
        '''
        Old and slow version of Board.get_words().
        '''
        result = []
        for cube in self.cubes_used:
            for path in cube.find_paths():
                if len(path) >= 3:
                    str_path = list_to_str(path).lower()
                    if str_path in self.words_set:
                        result.append(str_path)
        return result
    
    # 
    def get_words(self):
        '''
        Returns a list of all of the valid words (at least 3 letters long and in the dictionary) in the board.
        '''
        result = []
        for cube in self.cubes_used:
            for word in cube.find_words():
                if len(word) >= self.min_word_length and word not in result:
                    result.append(word)
        return result
    
    def get_points(self):
        acc = 0
        for word in self.all_words:
            if len(word) == 3: acc += 1
            elif len(word) == 4: acc += 1
            elif len(word) == 5: acc += 2
            elif len(word) == 6: acc += 3
            elif len(word) == 7: acc += 5
            elif len(word) >= 8: acc += 11
        return acc

class Cube:
    '''
        A cube with letters.

        Class variables:
        - letter_list: provided list of letters, specific to each cube
        - displayed_letter: letter that will display on board after rolling
        - neighbors: Cube objects next to self. Note it is very important that before a Cube's 
        neighbors are added its neighbors attribute is None, and not the empty list due to Python list mutation.
        '''
    def __init__(self, letter_list, board, neighbors=None):
        self.letter_list = letter_list
        self.board = board
        self.displayed_letter = None
        self.neighbors = neighbors

    def __repr__(self):
        return self.displayed_letter

    def roll(self):
        '''
        Rolls the Cube by randomly selecting one of its faces to display.
        '''
        self.displayed_letter = self.letter_list[random.randint(0, len(self.letter_list)-1)] # usually 6, but edited for testing so i don't have to add 6 faces

    def display_letter(self, letter):
        '''
        Sets the displayed letter of a Cube to a particular one of its faces.
        '''
        assert letter in self.letter_list
        self.displayed_letter = letter

    # 
    def add_neighbor(self, new):
        '''
        Adds new (a Cube instance) to the list self.neighbors and also adds self to new.neighbors. Instantiates neighbor lists if necessary.
        '''
        if self.neighbors is None:
            self.neighbors = []
        if new.neighbors is None:
            new.neighbors = []
        if new not in self.neighbors and self not in new.neighbors:
            self.neighbors.append(new)
            new.neighbors.append(self)
    
    def clear_neighbors(self):
        self.neighbors = None
    
    def find_paths(self):
        '''
        Outdated way to find paths beginning with self.
        '''
        return self.paths_helper([self])
    
    def paths_helper(self, current_path):
        '''
        Outdated helper function to find paths.
        '''
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
        '''
        Finds all valid words beginning with self.
        '''
        return self.words_helper([self])

    def words_helper(self, current_path):
        '''
        - Variant of DFS, where the Cubes are like graph vertices. 
        - Checks at each step if there are any valid words beginning with the current path (reduces 4x4 solve time from about 17 secs to about 0.0015 secs)
        '''
        current_str = list_to_str(current_path).lower()
        result = []
        if current_str in self.board.words_set:
            result.append(current_str)
        if self.neighbors is None:
            return result
        if len(current_str) >= 2 and current_str not in self.board.prefixes_set_list[len(current_str)-2]:
            pass
        else:
            for neighbor in self.neighbors:
                if neighbor not in current_path:
                    current_path.append(neighbor)
                    newpaths = neighbor.words_helper(current_path)
                    result.extend(newpaths)
        current_path.pop()
        return result

def list_to_str(input_list):
    '''
    Converts a list of Cubes a string of the displayed letters.
    '''
    result = ""
    for cube in input_list:
        result += cube.displayed_letter
    return result
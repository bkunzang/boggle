import random
import csv

class Board:
    def __init__(self, dim=4, csv_file="standard_board.csv"):
        '''
        A Boggle board.

        Class variables:
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

        self.cube_configuration = [[] for _ in range(dim)]
        self.dim = dim

#    def __repr__(self):
 #       for row in self.dim:
  #          print(row)

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
        
        # add neighbors to each cube
        for row in self.dim:
            for col in self.dim:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (row + i > 0) and (row + i < self.dim) and (col + j > 0) and (col + j < self.dim):
                            self.cube_configuration[row][col].neighbors.append(self.cube_configuration[row + i][col + i])

    # get a list of paths with length in range(min,max)
    def get_paths(self, min, max):
        result = []
        for cube in self.cubes_used:
            result.extend(cube.find_paths())
        return list(filter(lambda x: len(x) >= min and len(x) < max, result))

     # get all paths of length at least 4 and then turn them into strings (i am aware that i could do this nicer with the get_paths function with minimum 4 but i haven't fixed it yet)
    def get_words(self):
        result = []
        for cube in self.cubes_used:
            for path in cube.find_paths():
                if len(path) >= 4:
                    str_path = list_to_str(path)
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
    result = ''
    for cube in input_list:
        result += cube.displayed_letter
    return result
            
#test 3x3 board
a=Cube(['a'])
s=Cube(['s'])
e=Cube(['e'])
t=Cube(['t'])
r=Cube(['r'])
o=Cube(['o'])
w=Cube(['w'])
n=Cube(['n'])
m=Cube(['m'])
board = Board([a,s,e,t,r,o,w,n,m])
for cube in board.cubes_used:
    cube.roll()
for i in [s, t, r]:
    a.add_neighbor(i)
for i in [a, e, o, r, t]:
    s.add_neighbor(i)
for i in [a, s, r, w, n]:
    t.add_neighbor(i)
for i in [s, e, r, n, m]:
    o.add_neighbor(i)
for i in [a, s, e, t, o, w, n, m]:
    r.add_neighbor(i)
for i in [w, t, r, m, o]:
    n.add_neighbor(i)

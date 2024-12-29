class Board:
    def __init__(self, letter_list):
        self.letters = letter_list # list of letters in the board
    
    # get a list of paths with length in range(min,max)
    def get_paths(self, min, max):
        result = []
        for letter in self.letters:
            result.extend(letter.find_paths())
        return list(filter(lambda x: len(x) >= min and len(x) < max, result))

    # get all paths of length at least 4 and then turn them into strings (i am aware that i could do this nicer with the get_paths function with minimum 4 but i haven't fixed it yet)
    def get_words(self):
        result = []
        for letter in self.letters:
            for path in letter.find_paths():
                if len(path) >= 4:
                    str_path = list_to_str(path)
                    result.append(str_path)
        return result

# basically a graph
class Letter:
    def __init__(self, letter, neighbors=None):
        self.letter = letter
        self.neighbors = neighbors

    def __repr__(self):
        return self.letter

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
    for letter in input_list:
        result += letter.letter
    return result
            
#test 3x3 board
a=Letter('a')
s=Letter('s')
e=Letter('e')
t=Letter('t')
r=Letter('r')
o=Letter('o')
w=Letter('w')
n=Letter('n')
m=Letter('m')
board = Board([a,s,e,t,r,o,w,n,m])
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

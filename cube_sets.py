from word_finder import *
import numpy as np
import string
import multiprocessing
alphabet = list(string.ascii_letters[:26])
board = Board(dim=5, filtered=True)

def str_to_cube(letters_str):
    assert len(letters_str) == 6
    letters_list = [i+'u' if i == 'q' else i for i in letters_str]
    return Cube(letters_list, board)

def str_to_cubes(cube_str, dim=5):
    return [str_to_cube(cube_str[6*i:6*(i+1)]) for i in range(dim*dim)]

def cube_to_str(cube):
    result = []
    for letter in cube.letter_list:
        result += letter
    return result

def cubes_test(cubes, iters):
    board.change_cubes(cubes.cube_list)
    acc = 0
    for i in range(iters):
        board.populate()
        acc += board.total_points
    return acc / iters

def crossover(genome1, genome2):
    assert len(genome1) == len(genome2)
    index = np.random.uniform(0, len(genome1))
    child1 = genome1[:index] + genome2[index:]
    child2 = genome2[:index] + genome1[index:]
    return (child1, child2)

def run_cubes(cube_string, iters):
    cubes = str_to_cubes(cube_string)
    board.cube_configuration = cubes
    acc = 0
    for _ in range(iters):
        board.populate()
        acc += board.total_points
    return acc / iters

class CubeSet:
    def __init__(self, cube_string, dim=5):
        self.cube_string = cube_string
        self.cube_list = str_to_cubes(cube_string)
        self.dim = dim
        self.score = None

    def __str__(self):
        return self.cube_string
    
    def __repr__(self):
        return self.cube_string
    
    def is_legal(self):
        return all([i in self.cube_string for i in alphabet]) and len(self.cube_string) == 6*self.dim*self.dim

    def fitness(self, iters):
        if not self.is_legal():
            self.score = 0
            return 0
        board.change_cubes(self.cube_list)
        #words_set = set()
        #s_count = self.cube_string.count('s')
        #e_count = self.cube_string.count('e')
        acc = 0
        for _ in range(iters):
            board.populate()
            if board.num_words == 0:
                pass
            else:
                acc += board.long_words / board.num_words
            #acc += board.long_words / board.num_words - (2 ** (s_count - 9)) / 2500
        #size = len(words_set)
        mean = acc / iters
        adjusted = mean #- (2 ** (s_count - 9)) - (2 ** (e_count - 21))
        if adjusted < 0:
            adjusted = 0
        self.score = adjusted
        return adjusted
    
    def cubeset_to_csv(self):
        result_file = 'new_cubes.csv'
        for i in self.cube_list:
            i.letter_list = sorted(i.letter_list)
        with open(result_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            sorted_cube_list = sorted(self.cube_list, key=lambda x: ''.join(x.letter_list))
            for cube in sorted_cube_list:
                writer.writerow(list(map(lambda x: x.capitalize(), cube.letter_list)))

'''
def random_cubes():
    result = ''
    while True:
        for i in range(150):
            new_letter = np.random.choice(alphabet)
            result += new_letter
        if is_legal(result):
            return result
        result = ''
'''
class Genetic:
    def __init__(self, fitness=CubeSet.fitness, alphabet=alphabet, genome_length=150, population_size=500, mutation_rate=0.08, crossover_rate=0.7, population=None, generations = 700):
        self.fitness = fitness
        self.alphabet = alphabet
        self.genome_length = genome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = population
        self.generations = generations
        self.choices = ['crossover', 'mutate', 'copy']
        self.choice_probs = [crossover_rate, mutation_rate, 1-(mutation_rate+crossover_rate)]
        self.averages = []
        self.best = []

    def is_legal(self, input):
        return all([i in input for i in self.alphabet]) and len(input) == self.genome_length
    
    def crossover(self, set1, set2):
        genome1 = set1.cube_string
        genome2 = set2.cube_string
        while True:
            assert len(genome1) == self.genome_length and len(genome2) == self.genome_length
            index = np.random.randint(0, len(genome1))
            child1 = genome1[:index] + genome2[index:]
            child2 = genome2[:index] + genome1[index:]
            if self.is_legal(child1) and self.is_legal(child2):
                return (CubeSet(child1), CubeSet(child2))
    
    def mutate(self, genome):
        while True:
            index = np.random.uniform(0, len(genome))
            new = np.random.choice(self.alphabet)
            genome[index] = new
            if self.is_legal(genome):
                return genome
            
    def generate_initial(self):
        self.population = []
        for _ in range(self.population_size):
            result_list = []
            while True:
                result_list = []
                for _ in range(self.genome_length):
                    result_list.append(np.random.choice(self.alphabet))
                result_str = ''.join(result_list)
                if self.is_legal(result_str):
                    self.population.append(CubeSet(result_str))
                    break
        

    def run_generation(self):
        result = []
        for indiv in self.population:
            result.append(self.fitness(indiv, 6))
        return result
    
    def genetic_algorithm(self):
        self.generate_initial()
        for i in range(self.generations):
            result = self.run_generation()
            total = sum(result)
            probs = [result[i]/total for i in range(self.population_size)]
            print(len(self.population), len(probs), i)
            pool = [np.random.choice(self.population, p=probs) for _ in range(self.population_size)]
            new_pop = []
            while len(new_pop) < self.population_size:
                choice = np.random.choice(self.choices, p=self.choice_probs)
                if choice == 'copy':
                    new_pop.append(np.random.choice(pool))
                if choice == 'crossover':
                    parent1 = np.random.choice(pool)
                    parent2 = np.random.choice(pool)
                    children = self.crossover(parent1, parent2)
                    new_pop.extend(children)
                if choice == 'mutate':
                    res = ''
                    while not self.is_legal(res):
                        mutatee = np.random.choice(pool)
                        mutatee_genome = mutatee.cube_string
                        index = np.random.randint(0, 150)
                        new = np.random.choice(self.alphabet)
                        res = mutatee_genome[:index] + new + mutatee_genome[(index+1):]
                        res_cube = CubeSet(res)
                    new_pop.append(res_cube)
            if len(new_pop) > self.population_size:
                new_pop = new_pop[:self.population_size]
            self.population = new_pop
            self.average = total / self.population_size
            self.averages.append(self.average)
        result_file = 'cube_sets.csv'
        with open(result_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for i in self.population:
                i.score = self.fitness(i, 100)
                writer.writerow([i.cube_string, i.score])


'''
result_file = 'cube_sets.csv'
with open(result_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(csvfile)
        result = []
        for row in reader:
            cubeset = CubeSet(row[0])
            cubeset.fitness(100)
            result.append(cubeset)
'''





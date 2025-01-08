from word_finder import *
import numpy as np
import string
alphabet = list(string.ascii_letters[:26])
board = Board(dim=5)

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

def cubes_fitness(iters):
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
    def __init__(self, fitness=cubes_fitness, alphabet=alphabet, genome_length=150, population_size=100, mutation_rate=0.01, crossover_rate=0.07, population=None):
        self.fitness = fitness
        self.alphabet = alphabet
        self.genome_length = genome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = population

    def is_legal(self, input):
        return all([i in input for i in self.alphabet]) and len(input) == self.genome_length
    
    def crossover(self, genome1, genome2):
        while True:
            assert len(genome1) == self.genome_length and len(genome2) == self.genome_length
            index = np.random.uniform(0, len(genome1))
            child1 = genome1[:index] + genome2[index:]
            child2 = genome2[:index] + genome1[index:]
            if self.is_legal(child1) and self.is_legal(child2):
                return (child1, child2)
    
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
                    self.population.append(''.join(result_list))
                    break
        

    def run_generation(self):
        result = []
        for indiv in self.population:
            result.append(self.fitness(indiv))
        return result


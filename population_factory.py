import math

from numpy import random
from chromosome import Chromosome
from population import Population
from coding import encode


class PopulationFactory:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def generate_population(self, n, l, p_m, is_crossover):
        # if i < 1 or p_m == 0:
        chromosomes = [self.fitness_function.generate_optimal(l)]
        # else:
        #     chromosomes = []
        start = len(chromosomes)

        for j in range(start, n):
            code = random.binomial(n=1, p=.5, size=l)
            fitness = self.fitness_function.estimate(code)
            chromosomes.append(Chromosome(code, fitness, j+1))
        return Population(chromosomes, p_m, is_crossover)

    def generate_population_fx(self, n, l, p_m, is_crossover):
        # if i < 5 or p_m == 0:
        chromosomes = [self.fitness_function.generate_optimal(l)]
        # else:
        #     chromosomes = []
        start = len(chromosomes)

        fitness_list = random.binomial(n=self.fitness_function.b, p=.5, size=n-start)

        for y in fitness_list:
            x = round(y, 2)
            chromosomes.append(Chromosome(encode(x, self.fitness_function.a, self.fitness_function.b, l), float(x), start+1))
            start = start + 1

        return Population(chromosomes, p_m, is_crossover)

    def generate_population_fx2(self, n, l, p_m, is_crossover):
        # if i < 5 or p_m == 0:
        chromosomes = [self.fitness_function.generate_optimal(l)]
        # else:
        #     chromosomes = []
        start = len(chromosomes)

        fitness_list = random.binomial(n=(self.fitness_function.b*100)**2, p=.5, size=n-start)/10000

        for y in fitness_list:
            x = round(math.sqrt(y), 2)
            chromosomes.append(Chromosome(encode(x, self.fitness_function.a, self.fitness_function.b, l), float(x**2), start+1))
            start = start + 1

        return Population(chromosomes, p_m, is_crossover)

    def generate_population_f512(self, n, l, p_m, is_crossover):
        # if i < 5 or p_m == 0:
        chromosomes = [self.fitness_function.generate_optimal(l)]
        # else:
        #     chromosomes = []
        start = len(chromosomes)

        fitness_list = random.binomial(n=512**2, p=.5, size=n-start)/10000

        for y in fitness_list:
            x = round(math.sqrt(5.12 ** 2 - y), 2)
            chromosomes.append(Chromosome(encode(x, -5.12, 5.11, l), math.pow(5.12, 2) - math.pow(x, 2), start + 1))
            start = start + 1

        return Population(chromosomes, p_m, is_crossover)

    def generate_population_fecx(self, n, l, p_m,c, is_crossover):
        # if i < 5 or p_m == 0:
        chromosomes = [self.fitness_function.generate_optimal(l)]
        # else:
        #     chromosomes = []
        start = len(chromosomes)

        x_list = random.binomial(n=1023, p=.5, size=n-start)/100

        for x in x_list:
            chromosomes.append(Chromosome(encode(x, 0, 10.23, l), math.pow(math.e, c * x), start + 1))
            start = start + 1

        return Population(chromosomes, p_m, is_crossover)

    def generate_population_fhd(self, n, l, p_m, is_crossover):
        # if i < 5 or p_m == 0:
        chromosomes = [self.fitness_function.generate_optimal(l)]
        # else:
        #     chromosomes = []
        start = len(chromosomes)

        for j in range(start, n):
            code = random.binomial(n=1, p=.5, size=l)
            fitness = self.fitness_function.estimate(code)
            chromosomes.append(Chromosome(code, fitness, j+1))
        return Population(chromosomes, p_m, is_crossover)
#%%

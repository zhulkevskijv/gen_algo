import numpy as np
from chromosome import Chromosome
from constants import DELTA, SIGMA
from population_factory import PopulationFactory
from coding import *

class FConstALL:
    @staticmethod
    def get_genotype_value(chromosome_code):
        return np.count_nonzero(chromosome_code)

    def estimate(self, chromosome):
        return 100

    def generate_optimal(self, length):
        return Chromosome(np.zeros((length,), dtype=int), length)

    def generate_optimal_alt(self, length):
        return np.zeros((length,), dtype=int), length

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population(n, l, p_m, is_crossover)


class FHD:
    def __init__(self, delta):
        self.delta = delta

    @staticmethod
    def get_genotype_value(chromosome_code):
        return np.count_nonzero(chromosome_code)

    def estimate(self, chromosome):
        k = len(chromosome) - np.count_nonzero(chromosome)
        return (len(chromosome) - k) + k * self.delta

    def generate_optimal(self, length):
        return Chromosome(np.zeros((length,), dtype=int), length * self.delta)

    def generate_optimal_alt(self, length):
        return np.zeros((length,), dtype=int), length * self.delta

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population(n, l, p_m, is_crossover)


class Fx:
    def __init__(self, a, b, is_binary):
        self.a = a
        self.b = b
        self.is_binary = is_binary
        self.optimal_chromosome = None

    def estimate(self, chromosome):
        return decode(chromosome, self.a, self.b, len(chromosome), self.is_binary)

    def get_fenotype_value(self, chromosome_code):
        return decode(chromosome_code, self.a, self.b, len(chromosome_code), self.is_binary)

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def generate_optimal(self, length):
        if self.optimal_chromosome is None:
            gray_code = encode(self.b, self.a, self.b, length, self.is_binary)
            self.optimal_chromosome = Chromosome(gray_code, self.b)
        return Chromosome(self.optimal_chromosome.code.copy(), self.optimal_chromosome.fitness, self.optimal_chromosome.key)

    def generate_optimal_alt(self, length):
        if self.optimal_chromosome is None:
            gray_code = encode(self.b, self.a, self.b, length, self.is_binary)
            self.optimal_chromosome = Chromosome(gray_code, self.b)
        return np.array(self.optimal_chromosome.code.copy()), self.optimal_chromosome.fitness

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population(n, l, p_m, is_crossover)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b - ch.fitness) <= DELTA) and (decode(ch.code, self.a, self.b, len(ch.code), self.is_binary) - self.b) <= SIGMA

    def check_chromosome_success_alt(self, ch_code, ch_fitness):
        return ((self.b - ch_fitness) <= DELTA) and (
                    decode(ch_code, self.a, self.b, len(ch_code), self.is_binary) - self.b) <= SIGMA


class Fx2(Fx):
    def estimate(self, chromosome):
        return math.pow(decode(chromosome, self.a, self.b, len(chromosome), self.is_binary), 2)

    def generate_optimal(self, length):
        if self.optimal_chromosome is None:
            code = np.array(encode(self.b, self.a, self.b, length, self.is_binary))
            self.optimal_chromosome = Chromosome(code, math.pow(self.b, 2))
        return Chromosome(self.optimal_chromosome.code.copy(), self.optimal_chromosome.fitness, self.optimal_chromosome.key)
    def generate_optimal_alt(self, length):
        if self.optimal_chromosome is None:
            code = np.array(encode(self.b, self.a, self.b, length, self.is_binary))
            self.optimal_chromosome = Chromosome(code, math.pow(self.b, 2))
        return np.array(self.optimal_chromosome.code.copy()), self.optimal_chromosome.fitness

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population(n, l, p_m, is_crossover)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b ** 2 - ch.fitness) <= DELTA) and (decode(ch.code, self.a, self.b, len(ch.code), self.is_binary) - self.b) <= SIGMA

    def check_chromosome_success_alt(self, ch_code, ch_fitness):
        return ((self.b ** 2 - ch_fitness) <= DELTA) and (
                    decode(ch_code, self.a, self.b, len(ch_code), self.is_binary) - self.b) <= SIGMA


class F512subx2:
    def __init__(self, is_binary):
        self.is_binary = is_binary
        self.optimal_chromosome = None
    def estimate(self,chromosome):
        return math.pow(5.12, 2) - math.pow(decode(chromosome, -5.12, 5.11, len(chromosome), self.is_binary), 2)

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)
    def get_fenotype_value(self,chromosome_code):
        return decode(chromosome_code, -5.12, 5.11, len(chromosome_code), self.is_binary)

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        if self.optimal_chromosome is None:
            x = 0
            code = np.array(encode(x, -5.12, 5.11, length, self.is_binary))
            self.optimal_chromosome = Chromosome(code, math.pow(5.12, 2) - math.pow(decode(code, -5.12, 5.11, len(code), self.is_binary), 2))
        return Chromosome(self.optimal_chromosome.code.copy(), self.optimal_chromosome.fitness, self.optimal_chromosome.key)

    def generate_optimal_alt(self, length):
        if self.optimal_chromosome is None:
            x = 0
            code = np.array(encode(x, -5.12, 5.11, length, self.is_binary))
            self.optimal_chromosome = Chromosome(code, math.pow(5.12, 2) - math.pow(decode(code, -5.12, 5.11, len(code), self.is_binary), 2))
        return np.array(self.optimal_chromosome.code.copy()), self.optimal_chromosome.fitness

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population(n, l, p_m, is_crossover)

    def check_chromosome_success(self,ch: Chromosome):
        return (abs(math.pow(5.12, 2) - ch.fitness) <= DELTA) and abs(decode(ch.code, -5.12, 5.11, len(ch.code), self.is_binary)) <= SIGMA

    def check_chromosome_success_alt(self, ch_code, ch_fitness):
        return (abs(math.pow(5.12, 2) - ch_fitness) <= DELTA) and abs(
            decode(ch_code, -5.12, 5.11, len(ch_code), self.is_binary)) <= SIGMA


class Fecx:
    def __init__(self, c, is_binary):
        self.c = c
        self.is_binary = is_binary
        self.optimal_chromosome = None

    def estimate(self, chromosome_code):
        return math.pow(math.e, decode(chromosome_code, 0, 10.23, len(chromosome_code), self.is_binary) * self.c)

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def get_fenotype_value(self,chromosome_code):
        return decode(chromosome_code, 0, 10.23, len(chromosome_code), self.is_binary)

    # def get_genotype_value(self, chromosome_code):
    #     return to_decimal(chromosome_code, self.is_binary)

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_optimal(self, length):
        if self.optimal_chromosome is None:
            x = 10.23
            gray_code = np.array(encode(x, 0, 10.23, length, self.is_binary))
            self.optimal_chromosome = Chromosome(gray_code, math.pow(math.e, x * self.c))

        return Chromosome(self.optimal_chromosome.code.copy(), self.optimal_chromosome.fitness, self.optimal_chromosome.key)

    def generate_optimal_alt(self, length):
        if self.optimal_chromosome is None:
            x = 10.23
            gray_code = np.array(encode(x, 0, 10.23, length, self.is_binary))
            self.optimal_chromosome = Chromosome(gray_code, math.pow(math.e, x * self.c))

        return np.array(self.optimal_chromosome.code.copy()), self.optimal_chromosome.fitness

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population(n, l, p_m, is_crossover)

    def check_chromosome_success(self, ch: Chromosome):
        return (abs(math.pow(math.e, 10.23 * self.c) - ch.fitness) <= DELTA) and abs(decode(ch.code, 0, 10.23, len(ch.code), self.is_binary) - 10.23) <= SIGMA

    def check_chromosome_success_alt(self, ch_code, ch_fitness):
        return (abs(math.pow(math.e, 10.23 * self.c) - ch_fitness) <= DELTA) and abs(decode(ch_code, 0, 10.23, len(ch_code), self.is_binary) - 10.23) <= SIGMA
# %%

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

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population_fhd(n, l, p_m, is_crossover)


class Fx:
    def __init__(self, a, b, is_binary):
        self.a = a
        self.b = b
        self.is_binary = is_binary

    def estimate(self, chromosome):
        return decode(chromosome, self.a, self.b, len(chromosome), self.is_binary)

    def get_fenotype_value(self, chromosome_code):
        return decode(chromosome_code, self.a, self.b, len(chromosome_code), self.is_binary)

    def get_genotype_value(self, chromosome_code):
        return np.count_nonzero(chromosome_code)

    def generate_optimal(self, length):
        gray_code = encode(self.b, self.a, self.b, length)
        return Chromosome(gray_code, self.b)

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population_fx(n, l, p_m, is_crossover)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b - ch.fitness) <= DELTA) and (decode(ch.code, self.a, self.b, len(ch.code), self.is_binary) - self.b) <= SIGMA


class Fx2(Fx):
    def estimate(self, chromosome):
        if self.is_binary:
            return math.pow(decode(chromosome, self.a, self.b, len(chromosome), self.is_binary), 2)
        return math.pow(decode(chromosome, self.a, self.b, len(chromosome), self.is_binary), 2)

    def generate_optimal(self, length):
        code = np.array(encode(self.b, self.a, self.b, length, self.is_binary))
        return Chromosome(code, math.pow(self.b, 2))

    def get_optimal(self, l):
        return self.generate_optimal(l)

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population_fx2(n, l, p_m, is_crossover)

    def check_chromosome_success(self, ch: Chromosome):
        return ((self.b ** 2 - ch.fitness) <= DELTA) and (decode(ch.code, self.a, self.b, len(ch.code), self.is_binary) - self.b) <= SIGMA


class F512subx2:
    @staticmethod
    def estimate(chromosome):
        return math.pow(5.12, 2) - math.pow(decode(chromosome, -5.12, 5.11, len(chromosome)), 2)

    @staticmethod
    def get_genotype_value(chromosome_code):
        return decode(chromosome_code, -5.12, 5.11, len(chromosome_code))

    @staticmethod
    def get_optimal(l):
        return F512subx2.generate_optimal(l)

    @staticmethod
    def generate_optimal(length):
        x = 0
        gray_code = encode(x, -5.12, 5.11, length)
        return Chromosome(gray_code, math.pow(5.12, 2) - math.pow(decode(gray_code, -5.12, 5.11, len(gray_code)), 2))

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population_f512(n, l, p_m, is_crossover)

    @staticmethod
    def check_chromosome_success(ch: Chromosome):
        return (abs(math.pow(5.12, 2) - ch.fitness) <= DELTA) and abs(decode(ch.code, -5.12, 5.11, len(ch.code))) <= SIGMA

class Fecx:
    def __init__(self, c):
        self.c = c

    def estimate(self, chromosome_code):
        return math.pow(math.e, decode(chromosome_code, 0, 10.23, len(chromosome_code)) * self.c)

    @staticmethod
    def get_genotype_value(chromosome_code):
        return to_decimal(chromosome_code)

    @staticmethod
    def get_optimal(l):
        return F512subx2.generate_optimal(l)

    def generate_optimal(self, length):
        x = 10.23
        gray_code = encode(x, 0, 10.23, length)
        return Chromosome(gray_code, math.pow(math.e, x * self.c))

    def generate_population(self, n, l, p_m, is_crossover):
        return PopulationFactory(self).generate_population_fecx(n, l, p_m, self.c, is_crossover)

    def check_chromosome_success(self, ch: Chromosome):
        return (abs(math.pow(math.e, 10.23 * self.c) - ch.fitness) <= DELTA) and abs(decode(ch.code, 0, 10.23, len(ch.code)) - 10.23) <= SIGMA
# %%

from collections import deque

from population import Population
from statistics import mean
from constants import G
import math


class RWSAlt:
    @staticmethod
    def rws(population, fitness_func):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        probabilities = [fitness/population_fitness for fitness in population.fitness_list]
        population.update_rws(probabilities, fitness_func)

        return population

    def select(self, population, fitness_func):
        return self.rws(population,fitness_func)

    def get_name(self):
        return self.__class__.__name__


# class DisruptiveRWS:
#     @staticmethod
#     def disruptive_rws(population: Population):
#         population_fitness = sum(population.fitness_list)
#
#         if population_fitness == 0:
#             return population
#
#         f_avg = mean(population.fitness_list)
#         scaled_fitness = []
#
#         for chromosome in population.chromosomes:
#             scaled_fitness.append(abs(chromosome.fitness - f_avg))
#
#         sf_sum = sum(scaled_fitness)
#         if sf_sum > 0:
#             probabilities = [sf/sf_sum for sf in scaled_fitness]
#         else:
#             population_fitness = sum(population.fitness_list)
#             probabilities = [chromosome.fitness/population_fitness for chromosome in population.chromosomes]
#         population.update_rws(probabilities)
#
#         return population
#
#     def select(self, population):
#         return self.disruptive_rws(population)
#
#
# class BlendedRWS:
#     def __init__(self):
#         self.attempts = 0
#
#     def blended_rws(self, population: Population):
#         population_fitness = sum(population.fitness_list)
#
#         if population_fitness == 0:
#             return population
#
#         scaled_fitness = []
#
#         for chromosome in population.chromosomes:
#             scaled_value = chromosome.fitness / (G + 1 - self.attempts)
#             scaled_fitness.append(scaled_value)
#
#         sf_sum = sum(scaled_fitness)
#         probabilities = [sf/sf_sum for sf in scaled_fitness]
#         population.update_rws(probabilities)
#
#         return population
#
#     def select(self, population):
#         population = self.blended_rws(population)
#         self.attempts = self.attempts + 1
#         return population


class WindowRWSAlt:
    def __init__(self, h: int):
        self.fh_worst_list = deque()
        self.h = h

    def window_rws(self, population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        if len(self.fh_worst_list) > self.h:
            self.fh_worst_list.popleft()
        self.fh_worst_list.append(min(population.fitness_list))

        fh_worst = min(self.fh_worst_list)

        scaled_fitness = population.fitness_list - fh_worst

        sf_sum = sum(scaled_fitness)

        if sf_sum > 0:
            probabilities = scaled_fitness / sf_sum
        else:
            population_fitness = sum(population.fitness_list)
            probabilities = population.fitness_list / population_fitness

        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.window_rws(population)

    def get_name(self):
        return self.__class__.__name__+str(self.h)

class PowerLawRWSAlt:
    def __init__(self, k: float):
        self.k = k

    def power_law_rws(self, population: Population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        scaled_fitness = population.fitness_list ** self.k

        sf_sum = sum(scaled_fitness)

        if sf_sum > 0:
            probabilities = scaled_fitness / sf_sum
        else:
            probabilities = population.fitness_list / population_fitness
        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.power_law_rws(population)

    def get_name(self):
        return self.__class__.__name__+str(self.k)
#%%

from population import Population
from statistics import mean
from constants import G
import math


class RWS:
    @staticmethod
    def rws(population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        probabilities = [chromosome.fitness/population_fitness for chromosome in population.chromosomes]
        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.rws(population)


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


class WindowRWS:
    def __init__(self, h: int):
        self.fh_worst_list = []
        self.h = h

    def window_rws(self, population: Population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        if len(self.fh_worst_list) < self.h:
            self.fh_worst_list.append(min(population.fitness_list))
        else:
            self.fh_worst_list[1] = min(population.fitness_list)

        fh_worst = min(self.fh_worst_list)
        scaled_fitness = []

        for chromosome in population.chromosomes:
            scaled_value = chromosome.fitness - fh_worst
            scaled_fitness.append(scaled_value)

        sf_sum = sum(scaled_fitness)

        if sf_sum > 0:
            probabilities = [sf/sf_sum for sf in scaled_fitness]
        else:
            population_fitness = sum(population.fitness_list)
            probabilities = [chromosome.fitness/population_fitness for chromosome in population.chromosomes]

        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.window_rws(population)

    def get_name(self):
        return self.__class__.__name__+str(self.h)

class PowerLawRWS:
    def __init__(self, k: float):
        self.k = k

    def power_law_rws(self, population: Population):
        population_fitness = sum(population.fitness_list)

        if population_fitness == 0:
            return population

        scaled_fitness = []

        for chromosome in population.chromosomes:
            scaled_value = math.pow(chromosome.fitness , self.k)
            scaled_fitness.append(scaled_value)

        sf_sum = sum(scaled_fitness)
        if sf_sum > 0:
            probabilities = [sf/sf_sum for sf in scaled_fitness]
        else:
            population_fitness = sum(population.fitness_list)
            probabilities = [chromosome.fitness/population_fitness for chromosome in population.chromosomes]
        population.update_rws(probabilities)

        return population

    def select(self, population):
        return self.power_law_rws(population)

    def get_name(self):
        return self.__class__.__name__+str(self.k)
#%%

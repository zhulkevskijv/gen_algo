from constants import G
from population import Population
from numpy import random
from statistics import mean


def basic_sus(population: Population, total_fitness, fitness_scale:[]):
    mating_pool = []
    number_of_parents = len(population.chromosomes)
    fitness_step = total_fitness / number_of_parents
    random_offset = random.uniform(0, fitness_step)
    current_fitness_pointer = random_offset
    last_fitness_scale_position = 0

    for index in range(len(population.chromosomes)):
        for fitness_scale_position in range(last_fitness_scale_position, len(fitness_scale)):
            if fitness_scale[fitness_scale_position] >= current_fitness_pointer:
                mating_pool.append(population.chromosomes[fitness_scale_position])
                last_fitness_scale_position = fitness_scale_position
                break
        current_fitness_pointer += fitness_step

    return mating_pool


class SUS:
    @staticmethod
    def select(population: Population):
        total_fitness = 0
        fitness_scale = []

        for index, individual in enumerate(population.chromosomes):
            total_fitness += individual.fitness
            if index == 0:
                fitness_scale.append(individual.fitness)
            else:
                fitness_scale.append(individual.fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population


class DisruptiveSUS:
    @staticmethod
    def disruptive_sus(population: Population):
        total_fitness = 0
        fitness_scale = []
        f_avg = mean(population.fitness_list)

        for index, individual in enumerate(population.chromosomes):
            individual_scaled_fitness = abs(individual.fitness - f_avg)
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                fitness_scale.append(individual_scaled_fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population):
        return self.disruptive_sus(population)


class BlendedSUS:
    def __init__(self):
        self.attempts = 0

    def blended_sus(self, population: Population):
        total_fitness = 0
        fitness_scale = []

        for index, individual in enumerate(population.chromosomes):
            individual_scaled_fitness = individual.fitness / (G + 1 - self.attempts)
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                fitness_scale.append(individual_scaled_fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population):
        population = self.blended_sus(population)
        self.attempts = self.attempts + 1
        return population


class WindowSUS:
    def __init__(self, h: int):
        self.fh_worst_list = []
        self.h = h

    def window_sus(self, population: Population):
        total_fitness = 0
        fitness_scale = []

        if len(self.fh_worst_list) < self.h:
            self.fh_worst_list.append(min(population.fitness_list))
        else:
            self.fh_worst_list.pop(0)
            self.fh_worst_list.append(min(population.fitness_list))

        fh_worst = min(self.fh_worst_list)

        for index, individual in enumerate(population.chromosomes):
            individual_scaled_fitness = individual.fitness - fh_worst
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                fitness_scale.append(individual_scaled_fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population):
        return self.window_sus(population)

class PowerLawSUS:
    def __init__(self, h: int):
        self.fh_worst_list = []
        self.h = h

    def power_law_sus(self, population: Population):
        total_fitness = 0
        fitness_scale = []

        if len(self.fh_worst_list) < self.h:
            self.fh_worst_list.append(min(population.fitness_list))
        else:
            self.fh_worst_list.pop(0)
            self.fh_worst_list.append(min(population.fitness_list))

        fh_worst = min(self.fh_worst_list)

        for index, individual in enumerate(population.chromosomes):
            individual_scaled_fitness = individual.fitness - fh_worst
            total_fitness += individual_scaled_fitness
            if index == 0:
                fitness_scale.append(individual_scaled_fitness)
            else:
                fitness_scale.append(individual_scaled_fitness + fitness_scale[index - 1])

        mating_pool = basic_sus(population, total_fitness, fitness_scale)
        population.update_chromosomes(mating_pool)

        return population

    def select(self, population):
        return self.power_law_sus(population)
#%%

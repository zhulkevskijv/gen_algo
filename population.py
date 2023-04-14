import os
import random

import numpy as np
import seaborn as sns
from statistics import mean
import matplotlib.pyplot as plt

from constants import N, EPS


def all_the_same(elements):
    return len(elements) < 1 or len(elements) == elements.count(elements[0])


class Population:
    def __init__(self, chromosomes, p_m):
        self.chromosomes = chromosomes
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]
        self.p_m = p_m

    def print_fenotypes_distribution(self, folder_name, func_name, run, iteration):
        path = 'stats/' + folder_name + '/' + str(N) + '/' + func_name + '/' + str(run) + '/fenotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        sns.displot(self.fitness_list)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def print_genotypes_distribution(self, folder_name, func_name, run, iteration, fitness_func):
        path = 'stats/' + folder_name + '/' + str(N) + '/' + func_name + '/' + str(run) + '/genotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        x_list = [fitness_func.get_genotype_value(code) for code in self.genotypes_list]
        sns.displot(x_list)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def estimate_convergence(self, avg_fitness_list=None, last_n=None):
        if self.p_m == 0:
            return all_the_same(self.genotypes_list)
        else:
            if avg_fitness_list is None or last_n is None or len(avg_fitness_list) < last_n:
                return False

            last_n_avg_fitness_list = avg_fitness_list[-last_n:]
            last_n_diff = []

            for i in range(1, len(last_n_avg_fitness_list)):
                curr = last_n_avg_fitness_list[i]
                prev = last_n_avg_fitness_list[i-1]
                last_n_diff.append(abs(curr - prev))

            return all(x <= EPS for x in last_n_diff)

    def mutate(self, fitness_function):
        if self.p_m == 0:
            return
        for chromosome in self.chromosomes:
            for i in range(0, len(chromosome.code)):
                if random.random() < self.p_m:
                    chromosome.code[i] = int(not chromosome.code[i])
                    chromosome.fitness = fitness_function.estimate(chromosome.code)
        self.update()

    def get_mean_fitness(self):
        return mean(self.fitness_list)

    def get_max_fitness(self):
        return max(self.fitness_list)

    def get_best_genotype(self):
        max_value = self.get_max_fitness()
        best_list = list(filter(lambda x: self.fitness_list[x] == max_value, range(len(self.fitness_list))))
        return self.genotypes_list[best_list[0]]

    def get_fitness_std(self):
        return np.std(self.fitness_list)

    def get_unique_chromosomes_count(self):
        return len(set([chromosome.key for chromosome in self.chromosomes]))

    def get_keys_list(self):
        return list([chromosome.key for chromosome in self.chromosomes])

    def get_chromosomes_copies_count(self, chromosome_genotype):
        return self.genotypes_list.count(chromosome_genotype)

    def update(self):
        self.fitness_list = [chromosome.fitness for chromosome in self.chromosomes]
        self.genotypes_list = [list(x.code) for x in self.chromosomes]

    def update_rws(self, probabilities):
        self.chromosomes = [np.random.choice(self.chromosomes, p=probabilities) for _ in range(0,len(self.chromosomes))]
        self.update()

    def update_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.update()

    def __copy__(self):
        return Population(self.chromosomes.copy(), self.p_m.copy())
#%%

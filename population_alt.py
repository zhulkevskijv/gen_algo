import os

import numpy as np
import seaborn as sns
from statistics import mean
import matplotlib.pyplot as plt

from chromosome import Chromosome
from constants import MUTATION_LOW_LIMIT
from constants import EPS

from itertools import groupby

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def all_the_same(elements):
    return len(elements) < 1 or len(elements) == elements.count(elements[0])

hamming_limits = {
    'FConstALL': (0, 100),
    'FHD': (0, 100),
    'Fx2': (0, 10),
    'F512subx2': (0, 10),
    'Fecx': (0, 10),
    'exp_4': (0, 10),
    'exp_5': (0, 10),
}
x_limits = {
    'exp_1': (0, 11),
    'exp_2': (-6, 6),
    'exp_3': (0, 11),
    'exp_4': (0, 11),
    'exp_5': (0, 11),
}
y_limits = {
    'FConstALL': (0, 100),
    'FHD': (0, 10000),
    'Fx2': (0, 105),
    'F512subx2': (0, 27),
    'Fecx': (0, 13),
    'exp_4': (0, 27723),
    'exp_5': (0, 768_573_565),
}

class PopulationAlt:
    def __init__(self, chromosomes_codes, fitness_list, p_m, is_crossover):
        self.fitness_list = fitness_list
        self.genotypes_list = chromosomes_codes
        self.p_m = p_m
        self.is_crossover = is_crossover
        self.optimal_chromosome = chromosomes_codes[0]
        self.optimal_fitness = fitness_list[0]
        self.mutation_step_conv = 0
        self.keys = [i for i in range(len(chromosomes_codes))]

    def print_fenotypes_distribution(self, folder_name, func_name, run, iteration, fitness_func):
        fitness_func_name = fitness_func.__class__.__name__
        path = 'stats/' + folder_name + '/' + str(len(self.genotypes_list)) + '/' + func_name + '/' + str(run) + '/fenotypes'

        if not os.path.exists(path):
            os.makedirs(path)
        x_list = [fitness_func.get_fenotype_value(code) for code in self.genotypes_list]
        axis = sns.histplot(x_list)
        if fitness_func_name == 'FConstALL' or fitness_func_name =='FHD':
            axis.set_xlim(0,100)
        elif fitness_func_name == 'F512subx2':
            axis.set_xlim(-5.5, 5.5)
        else:
            axis.set_xlim(0, round(fitness_func.get_fenotype_value(fitness_func.generate_optimal_alt(10)[0]))+1)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def print_genotypes_distribution(self, folder_name, func_name, run, iteration, fitness_func):
        fitness_func_name = fitness_func.__class__.__name__
        path = 'stats/' + folder_name + '/' + str(len(self.genotypes_list)) + '/' + func_name + '/' + str(run) + '/genotypes'

        if not os.path.exists(path):
            os.makedirs(path)

        x_list = [fitness_func.get_genotype_value(code) for code in self.genotypes_list]

        if fitness_func_name == 'FHD':
            axis = sns.histplot(x_list, binwidth=5, binrange=(0, 100))
            axis.set_xlim(0, 100)
        else:
            axis = sns.histplot(x_list)
            if fitness_func_name == 'FConstALL':
                axis.set_xlim(0,100)
            else:
                axis.set_xlim(0, 10)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def print_fitness_f_distribution(self, folder_name, func_name, run, iteration, fitness_func):
        fitness_func_name = fitness_func.__class__.__name__
        path = 'stats/' + folder_name + '/' + str(len(self.genotypes_list)) + '/' + func_name + '/' + str(run) + '/fitness_values'
        if not os.path.exists(path):
            os.makedirs(path)
        if fitness_func_name == 'FHD':
            axis = sns.histplot(self.fitness_list, stat='count', binrange=(0, 10000), binwidth=500)
            axis.set_xlim(0, 10000)
        else:
            axis = sns.histplot(self.fitness_list, stat='count')
            if fitness_func_name == 'FConstALL':
                axis.set_xlim(0, fitness_func.generate_optimal_alt(100)[1])
            else:
                axis.set_xlim(0, round(fitness_func.generate_optimal_alt(10)[1])+1)
        plt.savefig(path + '/' + str(iteration) + '.png')
        plt.close()

    def estimate_convergence(self, avg_fitness_list=None, ff_name=None):
        if self.p_m == 0:
            # print(self.genotypes_list)
            return all_equal(self.genotypes_list)
        else:
            if 'FConstALL' in ff_name:
                # homogeneity
                return np.all(abs(self.genotypes_list.sum(axis=0) / len(self.genotypes_list) - 0.5) >= 0.49)
            else:
                if len(avg_fitness_list) < 2:
                    return False
                if abs(avg_fitness_list[-1] - avg_fitness_list[-2]) < EPS:
                    self.mutation_step_conv += 1
                else:
                    self.mutation_step_conv = 0
                if self.mutation_step_conv >= MUTATION_LOW_LIMIT:
                    return True

            return False

            # avg_fitness_list[-last_n:]
            #
            # for i in range(1, len(last_n_avg_fitness_list)):
            #     curr = last_n_avg_fitness_list[i]
            #     prev = last_n_avg_fitness_list[i-1]
            #     last_n_diff.append(abs(curr - prev))
            #
            # return all(x <= EPS for x in last_n_diff)

    def mutate(self, fitness_function):
        if self.p_m == 0:
            return
        self.genotypes_list[np.random.rand() <= self.p_m] ^= 1
        self.update(fitness_function)

    def crossover(self, fitness_function):
        if self.is_crossover:
            N = len(self.genotypes_list)
            indeces = np.random.choice(N //2, N // 2, replace=False)
            for index in indeces:
                crossover_point = np.random.choice(N-2, 1)[0]
                self.genotypes_list[index], self.genotypes_list[N-1-index] = np.concatenate((self.genotypes_list[index][0:crossover_point+1], self.genotypes_list[N-1-index][crossover_point+1: N]), axis=0), np.concatenate((self.genotypes_list[N-1-index][0:crossover_point+1],  self.chromosomes[index][crossover_point+1: N]), axis=0)
            self.update(fitness_function)

    def get_mean_fitness(self):
        return mean(self.fitness_list)

    def get_max_fitness(self):
        return max(self.fitness_list)

    def get_optim_num(self):
        optim_list = list(filter(lambda x: np.array_equal(x, self.optimal_chromosome.code), self.genotypes_list))
        return len(optim_list)

    def get_best_genotype(self):
        max_value_ind = np.argmax(self.fitness_list)
        return self.genotypes_list[max_value_ind]

    def get_fitness_std(self):
        return np.std(self.fitness_list)

    def get_unique_chromosomes_count(self):
        return len(set(self.keys))

    def get_keys_list(self):
        return self.keys

    def get_chromosomes_copies_count(self, chromosome_genotype):
        return self.genotypes_list.count(chromosome_genotype)

    def update(self, fitness_func):
        self.fitness_list = [fitness_func.estimate(chromosome) for chromosome in self.genotypes_list]

    def update_rws(self, probabilities, fitness_func):
        self.keys = np.random.choice(len(self.genotypes_list), len(self.genotypes_list), p=probabilities)
        self.genotypes_list = self.genotypes_list[self.keys]
        self.update(fitness_func)

    def update_chromosomes(self, chromosomes, fitness_func):
        self.genotypes_list = chromosomes
        self.update(fitness_func)
    def update_chromosomes_with_keys(self, mating_pool_keys, fitness_func):
        self.keys = mating_pool_keys
        self.genotypes_list = self.genotypes_list[mating_pool_keys]
        self.update(fitness_func)
    def update_keys(self):
        self.keys = [i for i in range(len(self.genotypes_list))]

    # def __copy__(self):
    #     return Population(self.chromosomes.copy(), self.p_m.copy(), self.is_crossover)
#%%

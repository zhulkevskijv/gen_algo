from pressure_stats import PressureStats
from noise_stats import NoiseStats
from selection_diff_stats import SelectionDiffStats
from reproduction_stats import ReproductionStats
from run import Run
from constants import *
from population_alt import *
from constants import runs_to_plot


class EvoAlgorithmAlt:
    def __init__(self, initial_population: PopulationAlt, selection_function, fitness_function, optimal, sf_name):
        self.population: PopulationAlt = initial_population
        self.selection_function = selection_function
        self.sf_name = sf_name
        self.iteration = 0
        self.pressure_stats = PressureStats()
        self.reproduction_stats = ReproductionStats()
        self.selection_diff_stats = SelectionDiffStats()
        self.noise_stats = NoiseStats()
        self.best = self.population.genotypes_list[0]
        self.pressure_stats.num_of_best.append(self.population.get_chromosomes_copies_count(self.best))
        self.pressure_stats.f_best.append(self.population.get_max_fitness())
        self.fitness_function = fitness_function
        self.optimal = optimal

    def run(self, run, folder_name, iterations_to_plot):
        avg_fitness_list = [self.population.get_mean_fitness()]
        std_fitness_list = [self.population.get_fitness_std()]
        best_fitness_list = [self.population.get_max_fitness()]
        optim_num_list = [self.population.get_optim_num()]
        stop = G
        if "FConstALL"  in self.fitness_function.__class__.__name__:
            stop = 2500
        convergent = self.population.estimate_convergence(avg_fitness_list, self.fitness_function.__class__.__name__)
        while not convergent and self.iteration < stop:
            if self.iteration < iterations_to_plot and run < runs_to_plot:
                if "FConstALL" not in self.fitness_function.__class__.__name__ and "FHD" not in self.fitness_function.__class__.__name__:
                    self.population.print_fenotypes_distribution(folder_name, self.sf_name, run + 1, self.iteration, self.fitness_function)
                self.population.print_genotypes_distribution(folder_name, self.sf_name, run + 1, self.iteration, self.fitness_function)
                self.population.print_fitness_f_distribution(folder_name, self.sf_name, run + 1, self.iteration, self.fitness_function)
            self.population.update_keys()
            keys_before_selection = self.population.get_keys_list()
            # best_genotype = self.population.genotypes_list[0] if run < 1 else self.population.get_best_genotype()
            f = avg_fitness_list[self.iteration]
            self.population = self.selection_function.select(self.population, self.fitness_function)
            keys_after_selection = self.population.get_keys_list()
            not_selected_chromosomes = set(keys_before_selection) - set(keys_after_selection)
            self.population.mutate(self.fitness_function)
            self.population.crossover(self.fitness_function)
            f_std = self.population.get_fitness_std()
            std_fitness_list.append(f_std)
            fs = self.population.get_mean_fitness()
            best_fs = self.population.get_max_fitness()
            optim_num = self.population.get_optim_num()
            avg_fitness_list.append(fs)
            best_fitness_list.append(best_fs)
            optim_num_list.append(optim_num)
            self.selection_diff_stats.s_list.append(fs - f)
            best_genotype = self.population.get_best_genotype()
            num_of_best = self.population.get_chromosomes_copies_count(best_genotype)
            self.reproduction_stats.rr_list.append(1 - (len(not_selected_chromosomes) / len(self.population.genotypes_list)))
            # self.reproduction_stats.best_rr_list.append(num_of_best / len(self.population.chromosomes))
            self.pressure_stats.intensities.append(PressureStats.calculate_intensity(fs, f, f_std))
            self.pressure_stats.f_best.append(self.population.get_max_fitness())
            self.pressure_stats.num_of_best.append(num_of_best)
            self.iteration += 1
            self.pressure_stats.grs.append(PressureStats.calculate_growth_rate(self.pressure_stats.num_of_best[self.iteration],
                                                                               self.pressure_stats.num_of_best[self.iteration-1],
                                                                               self.pressure_stats.f_best[self.iteration],
                                                                               self.pressure_stats.f_best[self.iteration-1]))
            if num_of_best >= len(self.population.genotypes_list) / 2 and self.pressure_stats.grl is None:
                self.pressure_stats.grli = self.iteration
                self.pressure_stats.grl = self.pressure_stats.grs[-1]
            convergent = self.population.estimate_convergence(avg_fitness_list, self.fitness_function.__class__.__name__)

        if convergent:
            self.pressure_stats.NI = self.iteration
            self.noise_stats.NI = self.iteration
        if run < runs_to_plot:
            if "FConstALL" not in self.fitness_function.__class__.__name__ and "FHD" not in self.fitness_function.__class__.__name__:
                self.population.print_fenotypes_distribution(folder_name, self.sf_name, run + 1, self.iteration, self.fitness_function)
            self.population.print_genotypes_distribution(folder_name, self.sf_name, run + 1, self.iteration, self.fitness_function)
            self.population.print_fitness_f_distribution(folder_name, self.sf_name, run + 1, self.iteration, self.fitness_function)
        self.reproduction_stats.calculate()
        if 'FConstALL' not in self.fitness_function.__class__.__name__:
            self.pressure_stats.takeover_time = self.iteration
            self.pressure_stats.f_found = self.population.get_max_fitness()
            self.pressure_stats.f_avg = self.population.get_mean_fitness()
            self.pressure_stats.calculate()
            self.selection_diff_stats.calculate()
        is_successful = self.check_success() if convergent else False

        return Run(avg_fitness_list, std_fitness_list, self.pressure_stats, self.reproduction_stats, self.selection_diff_stats, self.noise_stats, is_successful, best_fitness_list, optim_num_list)

    def check_success(self):
        ff_name = self.fitness_function.__class__.__name__
        if ff_name == 'FConstALL':
            return True
        elif ff_name == 'FH' or ff_name == 'FHD':
            if self.population.p_m == 0:
                return self.population.get_chromosomes_copies_count(list(self.optimal)) == len(self.population.genotypes_list)
            else:
                return self.population.get_chromosomes_copies_count(list(self.optimal)) >= (len(self.population.genotypes_list) * 0.9)

        else:
            return any([self.fitness_function.check_chromosome_success_alt(self.population.genotypes_list[i], self.population.fitness_list[i]) for i in range(len(self.population.fitness_list))])

    # @staticmethod
    # def calculate_noise(sf):
    #     pop = FConstALL().generate_population(N, 100, 0)
    #     population = Population(pop.chromosomes.copy(), pop.p_m)
    #     iteration = 0
    #     stop = G
    #
    #     if type(sf) == WindowRWS or type(sf) == WindowSUS:
    #         sf.fh_worst_list = []
    #
    #     while not population.estimate_convergence() and iteration < stop:
    #         population = sf.select(population)
    #         iteration += 1
    #
    #     ns = NoiseStats()
    #
    #     if population.estimate_convergence():
    #         ns.NI = iteration
    #         ns.conv_to = population.chromosomes[0].code
    #
    #     return ns
#%%

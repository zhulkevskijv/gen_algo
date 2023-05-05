from constants import MAX_RUNS
from runs_stats import RunsStats
from evoalgorithm import EvoAlgorithm
from population import Population
from excel import save_to_excel
from plots import *
import time
from tqdm import tqdm
from constants import iter_to_plot, runs_to_plot, mut_p_dict


def save_run_plots(ff_name, sf_name, run, iteration, N):
    save_line_plot(ff_name, sf_name, run.avg_fitness_list, 'avg_fitness' + str(iteration+1), 'Average fitness Value', iteration + 1, N)
    save_line_plot(ff_name, sf_name, run.best_fitness_list, 'best_fitness' + str(iteration+1), 'Best fitness value', iteration + 1, N)
    save_line_plot(ff_name, sf_name, run.std_fitness_list, 'std_fitness' + str(iteration + 1), 'Fitness Standard deviation', iteration + 1, N)
    save_line_plot(ff_name, sf_name, run.optim_num_list, 'optim_num' + str(iteration + 1), 'Optimal copies', iteration + 1, N)
    if ('FConstALL' not in ff_name):
        save_line_plot(ff_name, sf_name, run.pressure_stats.intensities, 'intensity' + str(iteration+1), 'Intensity', iteration + 1, N)
        save_line_plot(ff_name, sf_name, run.selection_diff_stats.s_list, 'selection_diff' + str(iteration+1),
                   'Selection difference', iteration + 1, N)
        save_lines_plot(ff_name, sf_name, [run.pressure_stats.intensities, run.selection_diff_stats.s_list],
                    ['Intensity', 'EvoAlgorithm diff'],
                    'intensity_and_sel_diff' + str(iteration+1), 'Intensity + EvoAlgorithm diff', iteration + 1, N)
        save_line_plot(ff_name, sf_name, run.pressure_stats.grs, 'growth_rate' + str(iteration+1), 'Growth rate', iteration + 1, N)
    save_lines_plot(ff_name, sf_name, [run.reproduction_stats.rr_list,
                                       [1 - rr for rr in run.reproduction_stats.rr_list]],
                    ['Reproduction rate', 'Loss of diversity'],
                    'repro_rate_and_loss_of_diversity' + str(iteration+1), 'Reproduction rate + Loss of diversity', iteration + 1, N)
    # save_line_plot(ff_name, sf_name, run.reproduction_stats.best_rr_list, 'best_chromosome_rate' + str(iteration+1),
    #                'Best chromosome rate', iteration + 1)


def main(fitness_function, selection_functions: [], file_name, *args):
    p_start = time.time()
    runs_dict = {}
    ff_name = file_name

    N = args[0]
    L = args[1]

    for selection_function in selection_functions:
        for i in range(4):
            if i == 0:
                runs_dict[selection_function.get_name()] = RunsStats()
            elif i == 1:
                runs_dict[selection_function.get_name()+'_mut'] = RunsStats()
            elif i == 2:
                runs_dict[selection_function.get_name() + '_cross'] = RunsStats()
            else:
                runs_dict[selection_function.get_name() + '_mut_cross'] = RunsStats()

    for i in tqdm(range(0, MAX_RUNS)):
        p = fitness_function.generate_population(*args, 0, True)

        for selection_function in selection_functions:
            for l in range(4):
                sf_name = ''
                if l == 0:
                    sf_name = selection_function.get_name()
                elif l == 1:
                    sf_name = selection_function.get_name()+'_mut'
                elif l == 2:
                    sf_name = selection_function.get_name()+ '_cross'
                else:
                    sf_name = selection_function.get_name()+ '_mut_cross'
                print(str(N)+' '+ff_name+' '+sf_name)

                sf = selection_function

                optimal = fitness_function.get_optimal(args[0])
                folder_name = file_name if file_name is not None else ff_name
                mutation_p = 0
                if l == 1 or l == 3:
                    mutation_p = mut_p_dict[L][N]
                # (0.00001 if ff_name == 'FConstALL' or ff_name == 'FHD' else 0.0001) if l == 1 or l == 3 else 0
                # print('before run')
                current_run = EvoAlgorithm(Population(p.chromosomes.copy(), mutation_p, is_crossover=l == 2 or l ==3), sf, fitness_function, optimal, sf_name).run(i, folder_name, iter_to_plot)
                # print('before save')
                if i < runs_to_plot:
                    save_run_plots(folder_name, sf_name, current_run, i, N)
                runs_dict[sf_name].runs.append(current_run)

    for selection_function in selection_functions:
        if 'FConstALL' not in (ff_name):
            for i in range(4):
                    if i == 0:
                        runs_dict[selection_function.get_name()].calculate()
                    elif i == 1:
                        runs_dict[selection_function.get_name() + '_mut'] .calculate()
                    elif i == 2:
                        runs_dict[selection_function.get_name() + '_cross'] .calculate()
                    else:
                        runs_dict[selection_function.get_name() + '_mut_cross'] .calculate()
        else:
            for i in range(4):
                    if i == 0:
                        runs_dict[selection_function.get_name()].calculate_const()
                    elif i == 1:
                        runs_dict[selection_function.get_name() + '_mut'] .calculate_const()
                    elif i == 2:
                        runs_dict[selection_function.get_name() + '_cross'] .calculate_const()
                    else:
                        runs_dict[selection_function.get_name() + '_mut_cross'] .calculate_const()
    # with open("files/sample.json", "a") as outfile:
    #     json.dump(runs_dict, outfile)

        # Reading from json file
        # json_object = json.load(openfile)
    # print(runs_dict)
    save_to_excel(runs_dict, file_name if file_name is not None else ff_name, N)

    p_end = time.time()
    print('Program ' + file_name + ' calculation (in sec.): ' + str((p_end - p_start)))

    return file_name, runs_dict

#%%

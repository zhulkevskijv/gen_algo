import time
from multiprocessing import Pool
from constants import fh_pm, fhd_pm, fx2_pm, env
from functions import *
from rws import RWS, WindowRWS, PowerLawRWS
from sus import SUS, WindowSUS, PowerLawSUS
from plots import *
from program import main, main_noise
from excel import save_avg_to_excel
from numpy import random


release_sm = [WindowRWS(2),WindowRWS(10), WindowSUS(2),WindowSUS(10), PowerLawRWS(1.005),PowerLawRWS(1.05), PowerLawSUS(1.005),PowerLawSUS(1.05)]
# testing_sm = [WindowRWS(2), WindowSUS(2)]
testing_sm = [
    # PowerLawSUS(1.005),
    # PowerLawSUS(1.05),
    WindowRWS(2),
WindowSUS(2)
]
selection_methods = testing_sm if env == 'test' else release_sm
release_functions = [
(FHD(100), selection_methods, 'FHD', N, 100)
    # (FConstALL(), selection_methods, 'FConstALL', N, 100)
    # (Fx2(0, 10.23), selection_methods, 'Fx2', N, 10),
# (F512subx2(), selection_methods, 'F512subx2', N, 10),
# (Fecx(0.25), selection_methods, 'Fecx025', N, 10),
#(Fecx(1), selection_methods, 'Fecx1', N, 10),
   # (Fecx(2), selection_methods, 'Fecx2', N, 10),
]
test_functions = [
    (FHD(100), selection_methods, 'FHD', N, 100)
    # (FConstALL(), selection_methods, 'FConstALL', N, 100)
    # (Fx2(0, 10.23), selection_methods, 'Fx2', N, 10),
# (F512subx2(), selection_methods, 'F512subx2', N, 10),
# (Fecx(0.25), selection_methods, 'Fecx025', N, 10),
#(Fecx(1), selection_methods, 'Fecx1', N, 10),
   # (Fecx(2), selection_methods, 'Fecx2', N, 10),
]
functions = test_functions if env == 'test' else release_functions
# functions = test_functions


if __name__ == '__main__':
    p_start = time.time()
    results = {}
    # noise_results = {}

    # with Pool(8) as p:
    for f in functions:
        res = main(*f)
        results[res[0]] = res[1]

        # noise_results['FConstA'] = main_noise(selection_methods)
        # save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%

import time
from multiprocessing import Pool, active_children
from constants import env
from functions import *
from rws import WindowRWS, PowerLawRWS
from sus import WindowSUS, PowerLawSUS
from program import main


release_sm = [WindowRWS(2),WindowRWS(10), WindowSUS(2),WindowSUS(10), PowerLawRWS(1.005),PowerLawRWS(1.05), PowerLawSUS(1.005),PowerLawSUS(1.05)]
testing_sm = [
    PowerLawSUS(1.005),
    # PowerLawSUS(1.05),
    PowerLawRWS(1.005),
    WindowRWS(2),
    WindowSUS(2),
]
selection_methods = testing_sm if env == 'test' else release_sm
release_functions = [
# (FHD(100), selection_methods, 'FHD', 100, 100),
# (FHD(100), selection_methods, 'FHD', 200, 100),
(FHD(100), selection_methods, 'FHD', 300, 100),
# (FHD(100), selection_methods, 'FHD', 400, 100),
    #     (FConstALL(), selection_methods, 'FConstALL', N, 100),
    #     (FConstALL(), selection_methods, 'FConstALL', 200, 100),
        (FConstALL(), selection_methods, 'FConstALL', 300, 100),
        # (FConstALL(), selection_methods, 'FConstALL', 400, 100),
    # (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 100, 10,),
    # (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 200, 10,),
    (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 300, 10,),
    # (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 400, 10,),
    #     (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 100, 10,),
    #     (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 200, 10,),
        (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 300, 10,),
        # (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 400, 10,),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 100, 10),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 200, 10),
(F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 300, 10),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 400, 10),
    # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 100, 10),
    # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 200, 10),
    (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 300, 10),
    # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 400, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 100, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 200, 10),
(Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 300, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 400, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 100, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 200, 10),
    (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 300, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 400, 10),
   # (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 100, 10),
   # (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 200, 10),
   (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 300, 10),
   # (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 400, 10),
    # (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 100, 10),
    # (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 200, 10),
    (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 300, 10),
    # (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 400, 10),
# (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 100, 10),
# (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 200, 10),
(Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 300, 10),
# (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 400, 10),
    #    (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 100, 10),
    #    (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 200, 10),
       (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 300, 10),
       # (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 400, 10),
]
test_functions = [
(FHD(100), selection_methods, 'FHD', 100, 100),
# (FHD(100), selection_methods, 'FHD', 200, 100),
# (FHD(100), selection_methods, 'FHD', 300, 100),
# (FHD(100), selection_methods, 'FHD', 400, 100),
    #     (FConstALL(), selection_methods, 'FConstALL', N, 100),
    #     (FConstALL(), selection_methods, 'FConstALL', 200, 100),
    #     (FConstALL(), selection_methods, 'FConstALL', 300, 100),
    #     (FConstALL(), selection_methods, 'FConstALL', 400, 100),
    # (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 100, 10,),
    # (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 200, 10,),
#     (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 300, 10,),
#     (Fx2(0, 10.23, is_binary=True), selection_methods, 'Fx2Bin', 400, 10,),
        #     (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 100, 10,),
        #     (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 200, 10,),
        #     (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 300, 10,),
        #     (Fx2(0, 10.23, is_binary=False), selection_methods, 'Fx2Gray', 400, 10,),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 100, 10),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 200, 10),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 300, 10),
# (F512subx2(is_binary=True), selection_methods, 'F512subx2Bin', 400, 10),
        # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 100, 10),
        # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 200, 10),
        # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 300, 10),
        # (F512subx2(is_binary=False), selection_methods, 'F512subx2Gray', 400, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 100, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 200, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 300, 10),
# (Fecx(0.25, is_binary=True), selection_methods, 'Fecx025Bin', 400, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 100, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 200, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 300, 10),
    # (Fecx(1, is_binary=True), selection_methods, 'Fecx1Bin', 400, 10),
    #    (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 100, 10),
    #    (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 200, 10),
    #    (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 300, 10),
    #    (Fecx(2, is_binary=True), selection_methods, 'Fecx2Bin', 400, 10),
# (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 100, 10),
# (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 200, 10),
# (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 300, 10),
# (Fecx(0.25, is_binary=False), selection_methods, 'Fecx025Gray', 400, 10),
#     (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 100, 10),
    # (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 200, 10),
    # (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 300, 10),
    # (Fecx(1, is_binary=False), selection_methods, 'Fecx1Gray', 400, 10),
    #    (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 100, 10),
       # (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 200, 10),
    #    (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 300, 10),
    #    (Fecx(2, is_binary=False), selection_methods, 'Fecx2Gray', 400, 10),
]
functions = test_functions if env == 'test' else release_functions
# functions = test_functions


if __name__ == '__main__':
    p_start = time.time()
    results = {}

    with Pool(12) as p:
        p.starmap(main, functions)
        # for f in functions:
        #     res = main(*f)
        #     results[res[0]] = res[1]

        # noise_results['FConstA'] = main_noise(selection_methods)
        # save_avg_to_excel(results, noise_results)

    p_end = time.time()
    print('Program calculation (in sec.): ' + str((p_end - p_start)))
#%%

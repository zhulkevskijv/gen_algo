env = 'test'
N = 100
G = 10000000
P_M = 0
EPS = 0.0001
MUTATION_LOW_LIMIT = 10
fh_pm = 5.63605E-06 if N == 1000 else 5.81669E-05
fhd_pm = 5.08066E-06 if N == 1000 else 6.26079E-05
fx2_pm = 1.22E-04 if N == 1000 else 7.97E-04
MAX_RUNS = 5 if env == 'test' else 10
SIGMA = DELTA = 0.01
#%%

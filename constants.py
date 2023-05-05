env = 'test1'
G = 10000
P_M = 0
EPS = 0.0001
MUTATION_LOW_LIMIT = 10
MAX_RUNS = 2 if env == 'test' else 100
SIGMA = DELTA = 0.01
iter_to_plot = 5
runs_to_plot = 5
mut_p_dict = {
  10: {
    100: 0.0001,
    200: 0.0001/2,
    300: 0.0001/3,
    400: 0.0001/4,
  },
  100: {
    100: 0.00001,
    200: 0.00001/2,
    300: 0.00001/3,
    400: 0.00001/4,
  }
}
#%%

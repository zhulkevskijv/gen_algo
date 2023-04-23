class Chromosome:
    def __init__(self, code, fitness, key=1):
        self.code = code
        self.fitness = fitness
        self.key = key

    def __str__(self):
        return "Fitness: " + str(self.fitness) + "\nCode: " + str(self.code) + "\nCode: " + str(self.code)

    def __repr__(self):
        return "Fitness: " + str(self.fitness) + "\nKey: " + str(self.key) + "\nCode: " + str(self.code)
#%%

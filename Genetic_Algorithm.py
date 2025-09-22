import random

N = 8

class GENETIC_ALGORITHM:
    def __init__(self, target, pop_size=100, mutation_rate=0.1, max_gen=1000):
        self.target = target              # target là ma trận 2D
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.max_gen = max_gen

    def random_state(self):
        state = [[0] * N for _ in range(N)]
        for i in range(N):
            c = random.randint(0, N-1)
            state[i][c] = 1
        return state

    def fitness(self, state):
        cost = 0
        for i in range(N):
            col_state = state[i].index(1)
            col_target = self.target[i].index(1)
            cost += abs(col_state - col_target)
        return cost

    def selection(self, population):
        total_fit = sum(1/(1+self.fitness(ind)) for ind in population)
        pick = random.uniform(0, total_fit)
        current = 0
        for ind in population:
            current += 1/(1+self.fitness(ind))
            if current > pick:
                return ind
        return population[-1]

    def crossover(self, p1, p2):
        point = random.randint(1, N-2)
        child1 = [row[:] for row in p1[:point]] + [row[:] for row in p2[point:]]
        child2 = [row[:] for row in p2[:point]] + [row[:] for row in p1[point:]]
        return child1, child2

    def mutate(self, state):
        if random.random() < self.mutation_rate:
            r = random.randint(0, N-1)
            c_old = state[r].index(1)
            c_new = random.randint(0, N-1)
            state[r][c_old] = 0
            state[r][c_new] = 1
        return state

    def run(self):
        population = [self.random_state() for _ in range(self.pop_size)]
        best = min(population, key=self.fitness)
        path = [best]

        for gen in range(self.max_gen):

            if best == self.target:
                print(f"Found solution at generation {gen}")
                return best, path

            new_population = []
            while len(new_population) < self.pop_size:
                p1 = self.selection(population)
                p2 = self.selection(population)
                c1, c2 = self.crossover(p1, p2)
                new_population.append(self.mutate(c1))
                new_population.append(self.mutate(c2))

            population = new_population
            best = min(population, key=self.fitness)
            path.append(best)

        print("Best found (not exact):")
        return best, path

def run_genetic_algorithm(target):
    ga = GENETIC_ALGORITHM(target, pop_size=200, mutation_rate=0.2, max_gen=2000)
    best, path = ga.run()
    return best, path




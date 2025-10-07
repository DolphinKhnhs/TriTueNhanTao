import random
import math
import time

N = 8

class LocalSearch:
    def __init__(self, target):
        self.target = target
        self.N = len(target)
        self.nodes_expanded = 0

    def manhattan_distance_rooks(self, board):
        distance = 0
        for r in range(self.N):
            if 1 in board[r]:
                c_current = board[r].index(1)
                c_target = self.target[r].index(1)
                distance += abs(c_current - c_target)
        return distance

    def random_state(self):
        state = [[0]*self.N for _ in range(self.N)]
        for i in range(self.N):
            c = random.randint(0, self.N-1)
            state[i][c] = 1
        return state

    def goal_test(self, state):
        return state == self.target

    # -------------------------
    # Hill Climbing
    # -------------------------
    def hill_climbing_rooks(self):
        start_time = time.time()
        self.nodes_expanded = 0
        state = self.random_state()
        initial_state = [row[:] for row in state]
        path = [state]

        while True:
            cost_curr = self.manhattan_distance_rooks(state)
            if cost_curr == 0:
                break
            neighbors = []
            for r in range(self.N):
                cur_col = state[r].index(1)
                for c in range(self.N):
                    if c != cur_col:
                        new_state = [row[:] for row in state]
                        new_state[r][cur_col] = 0
                        new_state[r][c] = 1
                        neighbors.append(new_state)
            self.nodes_expanded += len(neighbors)
            next_state = min(neighbors, key=self.manhattan_distance_rooks)
            if self.manhattan_distance_rooks(next_state) >= cost_curr:
                break
            state = next_state
            path.append(state)

        elapsed_time = time.time() - start_time
        return {
            "initial_state": initial_state,
            "path": path,
            "nodes_expanded": self.nodes_expanded,
            "time": elapsed_time
        }

    # -------------------------
    # Simulated Annealing
    # -------------------------
    def simulated_annealing_rooks(self, t_init=100, alpha=0.99):
        start_time = time.time()
        self.nodes_expanded = 0
        t = t_init
        state = self.random_state()
        initial_state = [row[:] for row in state]
        path = [state]

        while t > 0.001:
            cost_curr = self.manhattan_distance_rooks(state)
            if cost_curr == 0:
                break
            neighbors = []
            for r in range(self.N):
                cur_col = state[r].index(1)
                for c in range(self.N):
                    if c != cur_col:
                        new_state = [row[:] for row in state]
                        new_state[r][cur_col] = 0
                        new_state[r][c] = 1
                        neighbors.append(new_state)
            self.nodes_expanded += len(neighbors)
            next_state = min(neighbors, key=self.manhattan_distance_rooks)
            delta = self.manhattan_distance_rooks(next_state) - cost_curr
            if delta <= 0 or random.random() < math.exp(-delta / t):
                state = next_state
                path.append(state)
            t *= alpha

        elapsed_time = time.time() - start_time
        return {
            "initial_state": initial_state,
            "path": path,
            "nodes_expanded": self.nodes_expanded,
            "time": elapsed_time
        }

    # -------------------------
    # Genetic Algorithm
    # -------------------------
    def genetic_algorithm_rooks(self, pop_size=200, generations=2000, mutation_rate=0.2):
        start_time = time.time()
        self.nodes_expanded = 0
        self.max_frontier_size = pop_size

        def fitness(state):
            cost = 0
            for i in range(self.N):
                col_state = state[i].index(1)
                col_target = self.target[i].index(1)
                cost += abs(col_state - col_target)
            return cost

        def selection(population):
            total_fit = sum(1 / (1 + fitness(ind)) for ind in population)
            pick = random.uniform(0, total_fit)
            current = 0
            for ind in population:
                current += 1 / (1 + fitness(ind))
                if current > pick:
                    return ind
            return population[-1]

        def crossover(p1, p2):
            point = random.randint(1, self.N - 2)
            child1 = [row[:] for row in p1[:point]] + [row[:] for row in p2[point:]]
            child2 = [row[:] for row in p2[:point]] + [row[:] for row in p1[point:]]
            return child1, child2

        def mutate(state):
            if random.random() < mutation_rate:
                r = random.randint(0, self.N - 1)
                c_old = state[r].index(1)
                c_new = random.randint(0, self.N - 1)
                state[r][c_old] = 0
                state[r][c_new] = 1
            return state

        def random_state():
            state = [[0] * self.N for _ in range(self.N)]
            for i in range(self.N):
                c = random.randint(0, self.N - 1)
                state[i][c] = 1
            return state

        population = [random_state() for _ in range(pop_size)]
        best = min(population, key=fitness)
        initial_state = [row[:] for row in population[0]]
        path = [best]

        for _ in range(generations):
            if best == self.target:
                break
            new_population = []
            while len(new_population) < pop_size:
                p1 = selection(population)
                p2 = selection(population)
                c1, c2 = crossover(p1, p2)
                new_population.append(mutate(c1))
                new_population.append(mutate(c2))
            population = new_population
            self.nodes_expanded += len(population)
            best = min(population, key=fitness)
            path.append(best)

        elapsed_time = time.time() - start_time
        return {
            "initial_state": initial_state,
            "path": path,
            "nodes_expanded": self.nodes_expanded,
            "time": elapsed_time
        }

    # -------------------------
    # Beam Search
    # -------------------------
    def beam_search_rooks(self, k=5, max_iter=1000):
        start_time = time.time()
        self.nodes_expanded = 0
        states = [self.random_state() for _ in range(k)]
        initial_state = [row[:] for row in states[0]]
        path = [min(states, key=self.manhattan_distance_rooks)]

        for _ in range(max_iter):
            goal_found = False
            for s in states:
                if self.manhattan_distance_rooks(s) == 0:
                    goal_found = True
                    path.append(s)
                    break
            if goal_found:
                break
            all_neighbors = []
            for s in states:
                for r in range(self.N):
                    cur_col = s[r].index(1)
                    for c in range(self.N):
                        if c != cur_col:
                            new_state = [row[:] for row in s]
                            new_state[r][cur_col] = 0
                            new_state[r][c] = 1
                            all_neighbors.append(new_state)
            self.nodes_expanded += len(all_neighbors)
            states = sorted(all_neighbors, key=self.manhattan_distance_rooks)[:k]
            path.append(states[0])

        elapsed_time = time.time() - start_time
        return {
            "initial_state": initial_state,
            "path": path,
            "nodes_expanded": self.nodes_expanded,
            "time": elapsed_time
        }

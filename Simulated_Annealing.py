import math
import random

N = 8
class SUMULATED_ANNEALING:
    def __init__(self, target):
        self.target = target

    def random_state(self):
        state = [[0] * N for _ in range(N)]
        for i in range(N):
            c = random.randint(0, N-1)
            state[i][c] = 1
        return state

    def goal_test(self, state):
        return self.target == state

    def heuristic(self, state):
        cost = 0
        for i in range(N):
            if 1 in state[i]:
                col_state = state[i].index(1)
                if 1 in self.target[i]:
                    col_target = self.target[i].index(1)
                    cost += abs(col_state - col_target)
        return cost

    def create_neighbors(self, state):
        neighbors = []
        for r in range(N):
            cur_col = state[r].index(1)
            for c in range(N):
                if c != cur_col:
                    new_state = [row[:] for row in state]
                    new_state[r][cur_col] = 0   # xóa quân cũ
                    new_state[r][c] = 1        # đặt quân mới
                    neighbors.append(new_state)
        return neighbors

    def simulatedannealing(self):
        t=100
        alpha = 0.99
        state = self.random_state()
        path = [state]
        while t > 0.001:
            h_curr = self.heuristic(state)
            if h_curr == 0:
                return path

            neighbors = self.create_neighbors(state)
            next_state = min(neighbors, key=self.heuristic)
            next_h = self.heuristic(next_state)

            delta = next_h - h_curr
            if delta<=0:
                state = next_state
                path.append(state)
            else:
                probability = math.exp(-delta / t)
                if random.random() < probability:
                    state = next_state
                    path.append(state)
            t *= alpha
        return path


def run_simulated_annealing(target):
    sa = SUMULATED_ANNEALING(target)
    return sa.simulatedannealing()

import random

N = 8
class LOCAL_BEAM_SEARCH:
    def __init__(self, target, k = 5):
        self.target = target
        self.k = k

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
                    new_state[r][cur_col] = 0
                    new_state[r][c] = 1
                    neighbors.append(new_state)
        return neighbors

    def localbeamsearch(self, max_iter=1000):
        states = [self.random_state() for _ in range(self.k)]
        path = [min(states, key=self.heuristic)]

        for _ in range(max_iter):
            for s in states:
                if self.heuristic(s) == 0:
                    path.append(s)
                    return path

            all_neighbors = []
            for s in states:
                all_neighbors.extend(self.create_neighbors(s))

            states = sorted(all_neighbors, key=self.heuristic)[:self.k]

            best_state = states[0]
            path.append(best_state)

        return path


def run_local_beam_search(target, k):
    lbs = LOCAL_BEAM_SEARCH(target,k)
    return lbs.localbeamsearch(1500)

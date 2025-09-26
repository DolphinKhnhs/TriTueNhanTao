from DLS import DEPTH_LIMITED_SEARCH, Node, N

class ITERATIVE_LIMITED_SEARCH:
    def __init__(self, state, target):
        self.state = state
        self.target = target

    def search(self):
        for limit in range(N + 1):
            print(limit)
            dls = DEPTH_LIMITED_SEARCH(self.state, self.target, limit)
            result = dls.search(dls.initial)
            if isinstance(result, Node):
                return dls.solution(result)
        return None

def run_ids(initial, target):
    ids = ITERATIVE_LIMITED_SEARCH(initial, target)
    return ids.search()

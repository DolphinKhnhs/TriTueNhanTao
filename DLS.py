N = 8

class Node:
    def __init__(self, state, row=0, parent=None, depth=0):
        self.state = state
        self.row = row
        self.parent = parent
        self.depth = depth

class DEPTH_LIMITED_SEARCH:
    def __init__(self, state, target, limit=8):
        self.initial = Node(state)
        self.target = target
        self.limit = limit

    def search(self, node):
        if self.goal_test(node.state, self.target):
            return node
        elif node.depth == self.limit:
            return "cutoff"
        else:
            cutoff_occurred = False
            for child in self.create_child(node):
                result = self.search(child)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result != "failure":
                    return result
            return "cutoff" if cutoff_occurred else "failure"

    def create_child(self, node):
        list_child = []
        row = node.row
        for col in range(N):
            if self.is_safe(node.state, row, col):
                new_state = [r[:] for r in node.state]
                new_state[row][col] = 1
                child = Node(new_state, row + 1, parent=node, depth=node.depth + 1)
                list_child.append(child)
        return list_child

    def is_safe(self, state, row, col):
        for i in range(row):
            if state[i][col] == 1:
                return False
        return True

    def solution(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def goal_test(self, state, target):
        return state == target

def run_dls(initial, target):
    dls = DEPTH_LIMITED_SEARCH(initial, target, limit=8)
    result = dls.search(dls.initial)
    if isinstance(result, Node):
        return dls.solution(result)
    return result

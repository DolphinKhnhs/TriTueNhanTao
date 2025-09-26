from collections import deque

N = 8

class Node:
    def __init__(self, state, row=0, parent=None):
        self.state = state
        self.row = row
        self.parent = parent

class DEPTH_FIRST_SEARCH:
    def __init__(self, state, target):
        self.initial = state
        self.target = target
        self.frontier = deque([Node(state)])
        self.explored = set()

    def search(self):
        while self.frontier:
            node = self.frontier.pop()
            if self.goal_test(node.state, self.target) and node.row == N:
                return self.solution(node)
            print(node.state)
            self.explored.add(tuple(map(tuple, node.state)))

            if node.row < N:
                for child in self.create_child(node):
                    child_state = tuple(map(tuple, child.state))
                    if child_state not in self.explored and all(
                            tuple(map(tuple, n.state)) != child_state for n in self.frontier
                    ):
                        self.frontier.append(child)
        return None

    def create_child(self, node):
        list_child = []
        row = node.row
        for col in range(N):
            if self.is_safe(node.state, row, col):
                new_state = [r[:] for r in node.state]
                new_state[row][col] = 1
                child = Node(new_state, row + 1, parent=node)
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

def run_dfs(initial, target):
    dfs = DEPTH_FIRST_SEARCH(initial, target)
    return dfs.search()

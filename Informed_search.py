import time
import heapq
import itertools

class State:
    def __init__(self, board, row=0, parent=None, cost=0):
        self.board = [r[:] for r in board]
        self.row = row
        self.parent = parent
        self.cost = cost

    def is_goal(self, target):
        return self.board == target

    def get_path(self):
        path, node = [], self
        while node:
            path.append(node.board)
            node = node.parent
        return list(reversed(path))

def manhattan_distance_rooks(board, target):
    N = len(board)
    distance = 0
    for r in range(N):
        if 1 in board[r]:
            c_current = board[r].index(1)
            c_target = target[r].index(1)
            distance += abs(c_current - c_target)
    return distance

def greedy_rooks(target):
    start_time = time.time()
    N = len(target)
    root = State([[0]*N for _ in range(N)], 0, None, 0)

    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier, (manhattan_distance_rooks(root.board, target), next(counter), root))

    visited = {tuple(tuple(r) for r in root.board)}
    frontier_set = {tuple(tuple(r) for r in root.board)}

    nodes_expanded, max_frontier = 0, 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        h, _, state = heapq.heappop(frontier)
        board_tuple = tuple(tuple(r) for r in state.board)
        frontier_set.discard(board_tuple)
        nodes_expanded += 1

        if state.is_goal(target):
            return {
                "path": state.get_path(),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier,
                "time": time.time() - start_time,
                "heuristic": manhattan_distance_rooks(state.board, target),
                "cost": 0,
                "total_cost": state.cost
            }

        if state.row < N:
            for col in range(N):
                if all(state.board[r][col] == 0 for r in range(state.row)):
                    new_board = [r[:] for r in state.board]
                    new_board[state.row][col] = 1
                    board_tuple_new = tuple(tuple(r) for r in new_board)
                    if board_tuple_new not in visited and board_tuple_new not in frontier_set:
                        visited.add(board_tuple_new)
                        frontier_set.add(board_tuple_new)
                        heapq.heappush(frontier, (
                            manhattan_distance_rooks(new_board, target),
                            next(counter),
                            State(new_board, state.row + 1, state)
                        ))
    return None


def a_star_rooks(target):
    start_time = time.time()
    N = len(target)
    root = State([[0]*N for _ in range(N)], 0, None, 0)

    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier, (root.cost + manhattan_distance_rooks(root.board, target), next(counter), root))

    visited = dict()
    frontier_set = {tuple(tuple(r) for r in root.board)}

    nodes_expanded, max_frontier = 0, 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f, _, state = heapq.heappop(frontier)
        board_tuple = tuple(tuple(r) for r in state.board)
        frontier_set.discard(board_tuple)
        nodes_expanded += 1

        if state.is_goal(target):
            return {
                "path": state.get_path(),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier,
                "time": time.time() - start_time,
                "heuristic": manhattan_distance_rooks(state.board, target),
                "cost": state.cost,
                "total_cost": state.cost + manhattan_distance_rooks(state.board, target)
            }

        if state.row < N:
            for col in range(N):
                if all(state.board[r][col] == 0 for r in range(state.row)):
                    new_board = [r[:] for r in state.board]
                    new_board[state.row][col] = 1
                    board_tuple_new = tuple(tuple(r) for r in new_board)
                    g_new = state.cost + 1
                    h_new = manhattan_distance_rooks(new_board, target)
                    if (board_tuple_new not in visited or visited[board_tuple_new] > g_new) \
                            and board_tuple_new not in frontier_set:
                        visited[board_tuple_new] = g_new
                        frontier_set.add(board_tuple_new)
                        heapq.heappush(frontier, (g_new + h_new, next(counter), State(new_board, state.row + 1, state, g_new)))
    return None



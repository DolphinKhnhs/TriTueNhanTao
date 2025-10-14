import time
from collections import deque
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


def bfs_rooks(target):
    start_time = time.time()
    N = len(target)
    root = State([[0]*N for _ in range(N)], 0)

    frontier = deque([root])
    frontier_set = {tuple(tuple(r) for r in root.board)}
    visited = set()
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        state = frontier.popleft()
        frontier_set.remove(tuple(tuple(r) for r in state.board))
        nodes_expanded += 1

        if state.is_goal(target):
            end_time = time.time()
            return {
                "path": state.get_path(),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "time": end_time - start_time
            }

        row = state.row
        if row < N:
            for col in range(N):
                if all(state.board[r][col] == 0 for r in range(row)):
                    new_board = [r[:] for r in state.board]
                    new_board[row][col] = 1
                    child = State(new_board, row+1, state)

                    board_tuple = tuple(tuple(r) for r in child.board)
                    if board_tuple not in visited and board_tuple not in frontier_set:
                        visited.add(board_tuple)
                        frontier.append(child)
                        frontier_set.add(board_tuple)

        max_frontier_size = max(max_frontier_size, len(frontier))
    return None


def dfs_rooks(target):
    start_time = time.time()
    N = len(target)
    root = State([[0]*N for _ in range(N)], 0)

    frontier = deque([root])
    frontier_set = {tuple(tuple(r) for r in root.board)}
    visited = set()
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        state = frontier.pop()
        frontier_set.remove(tuple(tuple(r) for r in state.board))
        nodes_expanded += 1

        if state.is_goal(target):
            end_time = time.time()
            return {
                "path": state.get_path(),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "time": end_time - start_time
            }

        row = state.row
        if row < N:
            for col in range(N):
                if all(state.board[r][col] == 0 for r in range(row)):
                    new_board = [r[:] for r in state.board]
                    new_board[row][col] = 1
                    child = State(new_board, row+1, state)

                    board_tuple = tuple(tuple(r) for r in child.board)
                    if board_tuple not in visited and board_tuple not in frontier_set:
                        visited.add(board_tuple)
                        frontier.append(child)
                        frontier_set.add(board_tuple)

        max_frontier_size = max(max_frontier_size, len(frontier))
    return None

def manhattan_chain_cost(board):
    N = len(board)
    positions = []
    rows_with_rook = set()
    for r in range(N):
        for c in range(N):
            if board[r][c] == 1:
                positions.append((r, c))
                rows_with_rook.add(r)
    cost = 0
    for i in range(len(positions)-1):
        r1, c1 = positions[i]
        r2, c2 = positions[i+1]
        cost += abs(r1 - r2) + abs(c1 - c2)
    return cost


def ucs_rooks(target):
    start_time = time.time()
    N = len(target)
    root_board = [[0]*N for _ in range(N)]
    root_cost = manhattan_chain_cost(root_board)
    root = State(root_board, 0, None, root_cost)

    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier, (root.cost, next(counter), root))
    frontier_set = {tuple(tuple(r) for r in root.board)}
    visited = set()
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        cost_so_far, _, state = heapq.heappop(frontier)
        frontier_set.remove(tuple(tuple(r) for r in state.board))
        nodes_expanded += 1

        if state.is_goal(target):
            end_time = time.time()
            return {
                "path": state.get_path(),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "time": end_time - start_time,
            }
        row = state.row
        if row < N:
            for col in range(N):
                if all(state.board[r][col] == 0 for r in range(row)):
                    new_board = [r[:] for r in state.board]
                    new_board[row][col] = 1
                    child_cost = manhattan_chain_cost(new_board)
                    child = State(new_board, row+1, state, child_cost)

                    board_tuple = tuple(tuple(r) for r in child.board)
                    if board_tuple not in visited and board_tuple not in frontier_set:
                        heapq.heappush(frontier, (child.cost, next(counter), child))
                        frontier_set.add(board_tuple)

        visited.add(tuple(tuple(r) for r in state.board))
        max_frontier_size = max(max_frontier_size, len(frontier))

    return None


def dls_rooks(target, depth_limit=8):
    N = len(target)
    nodes_expanded = 0
    max_frontier_size = 0
    CUTOFF = "cutoff"
    FAILURE = "failure"

    start_time = time.time()

    def recursive_dls(state, depth):
        nonlocal nodes_expanded, max_frontier_size
        nodes_expanded += 1

        # Tính frontier = số node trên call stack
        current_frontier = depth + 1
        max_frontier_size = max(max_frontier_size, current_frontier)

        if state.is_goal(target):
            return state.get_path()
        if depth >= depth_limit:
            return CUTOFF

        row = state.row
        for col in range(N):
            if all(state.board[r][col] == 0 for r in range(row)):
                new_board = [r[:] for r in state.board]
                new_board[row][col] = 1
                child = State(new_board, row + 1, state)
                result = recursive_dls(child, depth + 1)
                if result == CUTOFF:
                    continue
                elif result != FAILURE:
                    return result

        return FAILURE

    root = State([[0]*N for _ in range(N)])
    result = recursive_dls(root, 0)
    end_time = time.time()

    output = {
        "nodes_expanded": nodes_expanded,
        "max_frontier_size": max_frontier_size,
        "time": end_time - start_time
    }

    if result == FAILURE:
        output["result"] = FAILURE
    else:
        output["result"] = "success"
        output["path"] = result

    return output


def ids_rooks(target, max_depth=None):
    N = len(target)
    if max_depth is None:
        max_depth = N

    start_time = time.time()
    total_nodes_expanded = 0
    overall_max_frontier = 0

    for depth in range(1, max_depth + 1):
        result = dls_rooks(target, depth)
        if result is None:
            continue
        total_nodes_expanded += result["nodes_expanded"]
        overall_max_frontier = max(overall_max_frontier, result.get("max_frontier_size", 0))
        if result["result"] == "success":
            end_time = time.time()
            return {
                "result": "success",
                "path": result["path"],
                "nodes_expanded": total_nodes_expanded,
                "max_frontier_size": overall_max_frontier,
                "time": end_time - start_time
            }
    end_time = time.time()
    return {
        "result": "failure",
        "nodes_expanded": total_nodes_expanded,
        "max_frontier_size": overall_max_frontier,
        "time": end_time - start_time
    }




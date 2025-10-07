import copy
import random
import time
from collections import deque

N = 8

class Node:
    def __init__(self, state, is_and_node=False, row=0):
        self.state = state
        self.is_and_node = is_and_node
        self.children = []
        self.parent = None
        self.row = row


class AndOrSearch:
    @staticmethod
    def and_or_search_rooks(state, target):
        start_time = time.time()
        node_expanded = 0

        def is_goal(state, target):
            return state == target

        def to_tuple(state):
            return tuple(map(tuple, state))

        def create_neighbors(state, row):
            """Sinh các trạng thái hàng tiếp theo, có yếu tố nhiễu nhẹ"""
            neighbors = []
            cols = list(range(N))
            random.shuffle(cols)

            for col in cols:
                if all(state[r][col] == 0 for r in range(N)):
                    new_state = copy.deepcopy(state)
                    new_state[row][col] = 1
                    neighbors.append(new_state)

                    # Tạo nhiễu nhẹ (xác suất thấp)
                    if random.random() < 0.1:
                        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = row + drow, col + dcol
                            if 0 <= nr < N and 0 <= nc < N and all(state[r][nc] == 0 for r in range(N)):
                                noisy_state = copy.deepcopy(state)
                                noisy_state[nr][nc] = 1
                                neighbors.append(noisy_state)
            return neighbors

        def or_search(state, row, path):
            nonlocal node_expanded
            if is_goal(state, target):
                return Node(state)

            if to_tuple(state) in path or row >= N:
                return None

            node_expanded += 1
            or_node = Node(state, is_and_node=False, row=row)

            for next_state in create_neighbors(state, row):
                and_node = Node(next_state, is_and_node=True, row=row)
                and_node.parent = or_node

                result_temp = and_search(next_state, row + 1, path | {to_tuple(state)})
                if result_temp:
                    and_node.children.append(result_temp)
                    or_node.children.append(and_node)
                    return or_node
            return None

        def and_search(state, row, path):
            return or_search(state, row, path)

        result = or_search(state, 0, set())
        end_time = time.time()

        if result:
            path = []
            current = result
            while current:
                path.append(current.state)
                if current.children:
                    current = current.children[0].children[0] if current.children[0].children else None
                else:
                    break

            return {
                "path": path,  # chỉ là list các ma trận
                "nodes_expanded": node_expanded,
                "time": round(end_time - start_time, 4),
                "solution_found": True
            }
        else:
            return {
                "path": None,
                "nodes_expanded": node_expanded,
                "time": round(end_time - start_time, 4),
                "solution_found": False
            }


def create_belief_state():
    belief_states = []
    for i in range(4):
        board = [[0 for _ in range(N)] for _ in range(N)]
        if i == 0:
            pass
        elif i == 1:
            row = random.randint(0, N - 1)
            col = random.randint(0, N - 1)
            board[row][col] = 1
        elif i == 2:
            for _ in range(2):
                while True:
                    row = random.randint(0, N - 1)
                    col = random.randint(0, N - 1)
                    if all(board[r][col] == 0 for r in range(N)):
                        board[row][col] = 1
                        break
        else:
            for _ in range(3):
                while True:
                    row = random.randint(0, N - 1)
                    col = random.randint(0, N - 1)
                    if all(board[r][col] == 0 for r in range(N)):
                        board[row][col] = 1
                        break
        belief_states.append((board, 0))  # Start from row 0 for all
    return belief_states


def is_goal(state, target):
    return state == target


def create_goal_state():
    """Create a valid goal state for 8 rooks"""
    board = [[0 for _ in range(N)] for _ in range(N)]
    cols = list(range(N))
    random.shuffle(cols)
    for row in range(N):
        board[row][cols[row]] = 1
    return board


def belief_state_search(target):
    start_time = time.time()

    init_belief_state = create_belief_state()
    frontier = deque()
    for belief, row in init_belief_state:
        frontier.append((belief, row))

    node_expanded = 0
    explored = set()
    path = []

    while frontier:
        belief, row = frontier.popleft()

        # Check if this belief state is goal
        if is_goal(belief, target):
            end_time = time.time()
            return {
                "path": path + [belief],
                "nodes_expanded": node_expanded,
                "time": end_time - start_time,
                "solution_found": True
            }

        if row >= N:
            continue

        node_expanded += 1

        # Generate next possible actions - placing rook in current row
        next_beliefs = []
        for col in range(N):
            # Check if column is available
            if all(belief[r][col] == 0 for r in range(N)):
                new_belief = copy.deepcopy(belief)
                new_belief[row][col] = 1
                next_beliefs.append((new_belief, row + 1))

        # Add to frontier if not explored
        for next_belief, next_row in next_beliefs:
            belief_hash = hash(tuple(tuple(row) for row in next_belief))
            if belief_hash not in explored:
                explored.add(belief_hash)
                frontier.append((next_belief, next_row))
                path.append(belief)

    end_time = time.time()
    return {
        "path": None,
        "nodes_expanded": node_expanded,
        "time": end_time - start_time,
        "solution_found": False
    }







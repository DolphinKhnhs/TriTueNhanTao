
import copy
import time
import random
from collections import deque

N = 8


class Backtracking:
    @staticmethod
    def is_safe(board):
        for r in range(N):
            if sum(board[r]) > 1:
                return False
        for c in range(N):
            if sum(board[r][c] for r in range(N)) > 1:
                return False
        return True

    @staticmethod
    def get_possible(board, row):
        moves = []
        cols = list(range(N))
        random.shuffle(cols)
        for col in cols:
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = 1
            moves.append(temp_board)
        return moves

    @staticmethod
    def backtrack(board, path=None, rows_remaining=None, nodes_expanded=0):
        if path is None:
            path = []
        if rows_remaining is None:
            rows_remaining = list(range(N))

        if not rows_remaining:
            return path, nodes_expanded

        if not Backtracking.is_safe(board):
            return None, nodes_expanded

        row = random.choice(rows_remaining)
        next_rows = [r for r in rows_remaining if r != row]

        for next_board in Backtracking.get_possible(board, row):
            nodes_expanded += 1
            if next_board not in path:
                path.append(next_board)
                result, nodes_expanded = Backtracking.backtrack(next_board, path, next_rows, nodes_expanded)
                if result:
                    return result, nodes_expanded
                path.pop()
        return None, nodes_expanded

    @staticmethod
    def board_to_str(board):
        return ["".join("Q" if x == 1 else "." for x in row) for row in board]

    @staticmethod
    def solve_eight_rooks():
        board = [[0] * N for _ in range(N)]
        start_time = time.time()
        solution_path, nodes_expanded = Backtracking.backtrack(board)
        end_time = time.time()

        return {
            "node_expanded": nodes_expanded,
            "time": end_time - start_time,
            "path": [Backtracking.board_to_str(b) for b in solution_path] if solution_path else []
        }

class Forward_checking:
    @staticmethod
    def is_safe(board):
        for r in range(N):
            if sum(board[r]) > 1:
                return False
        for c in range(N):
            if sum(board[r][c] for r in range(N)) > 1:
                return False
        return True

    @staticmethod
    def get_possible(board, row):
        moves = []
        cols = list(range(N))
        random.shuffle(cols)
        for col in cols:
            if Forward_checking.is_safe(board):
                temp_board = copy.deepcopy(board)
                temp_board[row][col] = 1
                moves.append(temp_board)
        return moves

    @staticmethod
    def backtrack(board, path=None, rows_remaining=None, nodes_expanded=0):
        if path is None:
            path = []
        if rows_remaining is None:
            rows_remaining = list(range(N))

        if not rows_remaining:
            return path, nodes_expanded

        row = random.choice(rows_remaining)
        next_rows = [r for r in rows_remaining if r != row]

        for next_board in Backtracking.get_possible(board, row):
            nodes_expanded += 1
            if next_board not in path:
                path.append(next_board)
                result, nodes_expanded = Backtracking.backtrack(next_board, path, next_rows, nodes_expanded)
                if result:
                    return result, nodes_expanded
                path.pop()
        return None, nodes_expanded

    @staticmethod
    def board_to_str(board):
        return ["".join("Q" if x == 1 else "." for x in row) for row in board]

    @staticmethod
    def solve_eight_rooks():
        board = [[0] * N for _ in range(N)]
        start_time = time.time()
        solution_path, nodes_expanded = Backtracking.backtrack(board)
        end_time = time.time()

        return {
            "node_expanded": nodes_expanded,
            "time": end_time - start_time,
            "path": [Backtracking.board_to_str(b) for b in solution_path] if solution_path else []
        }


class AC3RooksSolver:
    def __init__(self):
        self.N = 8
        self.variables = list(range(N))
        self.arcs = [(i, j) for i in self.variables for j in self.variables if i != j]
        random.shuffle(self.arcs)
        self.path = []  # Lưu lại các bước gán (row -> col)

    # Hàm revise: loại bỏ giá trị x của Xi nếu không tồn tại y trong Xj sao cho Xi != Xj
    def revise(self, d, xi, xj):
        revised = False
        to_remove = set()
        for x in d[xi]:
            if all(x == y for y in d[xj]):  # nếu tất cả giá trị y trong Xj đều vi phạm
                to_remove.add(x)
        if to_remove:
            d[xi] -= to_remove
            revised = True
        return revised

    # Thuật toán AC-3
    def ac3(self, d, arcs):
        queue = deque(random.sample(list(arcs), len(arcs)))
        while queue:
            xi, xj = queue.popleft()
            if self.revise(d, xi, xj):
                if len(d[xi]) == 0:
                    return False
                for xk in self.variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True

    # Backtracking có AC-3 hỗ trợ
    def backtrack(self, d):
        if all(len(d[row]) == 1 for row in self.variables):
            solution = [[0] * self.N for _ in range(self.N)]
            for row in self.variables:
                col = list(d[row])[0]
                solution[row][col] = 1
            return solution

        row = min((r for r in self.variables if len(d[r]) > 1),
                  key=lambda r: len(d[r]))

        for col in random.sample(list(d[row]), len(d[row])):
            new_domains = copy.deepcopy(d)
            new_domains[row] = {col}
            self.path.append((row, col))

            if self.ac3(new_domains, self.arcs):
                solution = self.backtrack(new_domains)
                if solution:
                    return solution

            self.path.pop()

        return None

    # Hàm solve trả về dict kết quả
    def solve(self):
        d = {row: set(range(self.N)) for row in self.variables}
        start = time.time()
        solution = self.backtrack(d)
        end = time.time()

        result = {
            "solution": solution,
            "path": self.path.copy(),
            "elapsed_time": round(end - start, 6)
        }
        return result








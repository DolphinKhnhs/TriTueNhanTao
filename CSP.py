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
    def backtrack(board, path=None, rows_remaining=None, nodes_expanded=0, max_frontier_size=0):
        if path is None:
            path = []
        if rows_remaining is None:
            rows_remaining = list(range(N))

        # Đếm node hiện tại
        current_nodes_expanded = nodes_expanded + 1

        if not rows_remaining:
            return path, current_nodes_expanded, max_frontier_size

        if not Backtracking.is_safe(board):
            return None, current_nodes_expanded, max_frontier_size

        row = random.choice(rows_remaining)
        next_rows = [r for r in rows_remaining if r != row]

        possible_moves = Backtracking.get_possible(board, row)
        current_frontier_size = len(possible_moves)
        max_frontier_size = max(max_frontier_size, current_frontier_size)

        for next_board in possible_moves:
            if next_board not in path:
                path.append(next_board)
                result, final_nodes_expanded, final_max_frontier = Backtracking.backtrack(
                    next_board, path, next_rows, current_nodes_expanded, max_frontier_size)
                if result:
                    return result, final_nodes_expanded, final_max_frontier
                path.pop()

            # Cập nhật nodes_expanded cho lần lặp tiếp theo
            current_nodes_expanded = max(current_nodes_expanded, nodes_expanded + 1)

        return None, current_nodes_expanded, max_frontier_size

    @staticmethod
    def solve_eight_rooks():
        board = [[0] * N for _ in range(N)]
        start_time = time.time()
        solution_path, nodes_expanded, max_frontier_size = Backtracking.backtrack(board)
        end_time = time.time()

        return {
            "node_expanded": nodes_expanded,
            "max_frontier_size": max_frontier_size,
            "time": end_time - start_time,
            "path": solution_path if solution_path else []
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
            temp_board = copy.deepcopy(board)
            temp_board[row][col] = 1
            if Forward_checking.is_safe(temp_board):
                moves.append(temp_board)
        return moves

    @staticmethod
    def backtrack(board, path=None, rows_remaining=None, nodes_expanded=0, max_frontier_size=0):
        if path is None:
            path = []
        if rows_remaining is None:
            rows_remaining = list(range(N))

        # Đếm node hiện tại
        current_nodes_expanded = nodes_expanded + 1

        if not rows_remaining:
            return path, current_nodes_expanded, max_frontier_size

        row = random.choice(rows_remaining)
        next_rows = [r for r in rows_remaining if r != row]

        possible_moves = Forward_checking.get_possible(board, row)
        current_frontier_size = len(possible_moves)
        max_frontier_size = max(max_frontier_size, current_frontier_size)

        for next_board in possible_moves:
            if next_board not in path:
                path.append(next_board)
                result, final_nodes_expanded, final_max_frontier = Forward_checking.backtrack(
                    next_board, path, next_rows, current_nodes_expanded, max_frontier_size)
                if result:
                    return result, final_nodes_expanded, final_max_frontier
                path.pop()

            # Cập nhật nodes_expanded cho lần lặp tiếp theo
            current_nodes_expanded = max(current_nodes_expanded, nodes_expanded + 1)

        return None, current_nodes_expanded, max_frontier_size

    @staticmethod
    def solve_eight_rooks():
        board = [[0] * N for _ in range(N)]
        start_time = time.time()
        solution_path, nodes_expanded, max_frontier_size = Forward_checking.backtrack(board)
        end_time = time.time()

        return {
            "node_expanded": nodes_expanded,
            "max_frontier_size": max_frontier_size,
            "time": end_time - start_time,
            "path": solution_path if solution_path else []
        }


class AC3RooksSolver:
    def __init__(self):
        self.N = 8
        self.variables = list(range(N))
        self.arcs = [(i, j) for i in self.variables for j in self.variables if i != j]
        random.shuffle(self.arcs)
        self.path = []
        self.max_frontier_size = 0
        self.nodes_expanded = 0

    def revise(self, d, xi, xj):
        """Sửa lại hàm revise cho đúng - constraint: các rook không cùng cột"""
        revised = False
        to_remove = set()

        # Nếu xj chỉ có 1 giá trị duy nhất, thì xi không thể có giá trị đó
        if len(d[xj]) == 1:
            conflicting_value = next(iter(d[xj]))
            if conflicting_value in d[xi]:
                to_remove.add(conflicting_value)
                revised = True

        if to_remove:
            d[xi] -= to_remove

        return revised

    def ac3(self, d):
        """Chạy thuật toán AC-3"""
        queue = deque(self.arcs.copy())

        while queue:
            xi, xj = queue.popleft()

            if self.revise(d, xi, xj):
                if len(d[xi]) == 0:
                    return False

                # Thêm các arc (xk, xi) với k khác i và j
                for xk in self.variables:
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))

        return True

    def create_board_from_domains(self, d):
        """Tạo board từ domains - chỉ hiển thị các giá trị đã được gán chắc chắn"""
        board = [[0] * self.N for _ in range(self.N)]
        for row in self.variables:
            if len(d[row]) == 1:
                col = list(d[row])[0]
                board[row][col] = 1
        return board

    def backtrack(self, d):
        """Backtracking với AC-3"""
        self.nodes_expanded += 1

        # Kiểm tra nếu tất cả variables đã được gán
        if all(len(d[row]) == 1 for row in self.variables):
            solution = [[0] * self.N for _ in range(self.N)]
            for row in self.variables:
                col = list(d[row])[0]
                solution[row][col] = 1
            # Thêm solution cuối cùng vào path
            if not self.path or self.path[-1] != solution:
                self.path.append(copy.deepcopy(solution))
            return solution

        # Chọn variable chưa được gán với MRV (Minimum Remaining Values)
        unassigned_rows = [r for r in self.variables if len(d[r]) > 1]
        if not unassigned_rows:
            return None

        row = min(unassigned_rows, key=lambda r: len(d[r]))

        # Lưu domains gốc để backtrack
        original_domains = copy.deepcopy(d)

        current_frontier = 0
        for col in list(d[row]):  # Dùng list để tránh modify during iteration
            current_frontier += 1

            # Tạo domains mới với giá trị đã chọn
            new_domains = copy.deepcopy(original_domains)
            new_domains[row] = {col}  # Gán giá trị cho hàng hiện tại

            # Thêm vào path TRƯỚC KHI chạy AC-3
            current_board = self.create_board_from_domains(new_domains)
            if not self.path or self.path[-1] != current_board:
                self.path.append(copy.deepcopy(current_board))

            # Chạy AC-3 để giảm domains
            if self.ac3(new_domains):
                # Gọi đệ quy
                solution = self.backtrack(new_domains)
                if solution is not None:
                    return solution

            # Backtrack: xóa khỏi path nếu không thành công
            if self.path and self.path[-1] == current_board:
                self.path.pop()

        # Cập nhật max frontier size
        self.max_frontier_size = max(self.max_frontier_size, current_frontier)

        return None

    def solve(self):
        """Giải bài toán 8 rooks bằng AC-3 + Backtracking"""
        # Khởi tạo domains: mỗi hàng có thể có rook ở bất kỳ cột nào
        domains = {row: set(range(self.N)) for row in self.variables}

        # Reset counters
        self.max_frontier_size = 0
        self.nodes_expanded = 0
        self.path = []

        # Thêm board rỗng đầu tiên vào path
        initial_board = [[0] * self.N for _ in range(self.N)]
        self.path.append(initial_board)

        start = time.time()

        # Chạy AC-3 trước để giảm domains
        if not self.ac3(domains):
            end = time.time()
            return {
                "solution": None,
                "path": self.path,
                "elapsed_time": end - start,
                "node_expanded": self.nodes_expanded,
                "max_frontier_size": self.max_frontier_size
            }

        # Sau đó chạy backtracking
        solution = self.backtrack(domains)
        end = time.time()

        # Đảm bảo path có solution cuối cùng
        if solution and (not self.path or self.path[-1] != solution):
            self.path.append(solution)

        return {
            "solution": solution,
            "path": self.path,
            "elapsed_time": end - start,
            "node_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size
        }


# Test các giải thuật
if __name__ == "__main__":
    print("=== BACKTRACKING ===")
    result_bt = Backtracking.solve_eight_rooks()
    print(f"Nodes expanded: {result_bt['node_expanded']}")
    print(f"Max frontier size: {result_bt['max_frontier_size']}")
    print(f"Time: {result_bt['time']:.6f}s")
    print(f"Path length: {len(result_bt['path'])}")
    if result_bt['path']:
        rook_count = sum(sum(row) for row in result_bt['path'][-1])
        print(f"Final solution has {rook_count}/8 rooks")

    print("\n=== FORWARD CHECKING ===")
    result_fc = Forward_checking.solve_eight_rooks()
    print(f"Nodes expanded: {result_fc['node_expanded']}")
    print(f"Max frontier size: {result_fc['max_frontier_size']}")
    print(f"Time: {result_fc['time']:.6f}s")
    print(f"Path length: {len(result_fc['path'])}")
    if result_fc['path']:
        rook_count = sum(sum(row) for row in result_fc['path'][-1])
        print(f"Final solution has {rook_count}/8 rooks")

    print("\n=== AC-3 ===")
    solver_ac3 = AC3RooksSolver()
    result_ac3 = solver_ac3.solve()
    print(f"Nodes expanded: {result_ac3['node_expanded']}")
    print(f"Max frontier size: {result_ac3['max_frontier_size']}")
    print(f"Time: {result_ac3['elapsed_time']:.6f}s")
    print(f"Path length: {len(result_ac3['path'])}")

    if result_ac3['solution']:
        rook_count = sum(sum(row) for row in result_ac3['solution'])
        print(f"Solution has {rook_count}/8 rooks")

        # Hiển thị chi tiết từng bước
        print("\nPath steps detail:")
        for i, board in enumerate(result_ac3['path']):
            rooks_in_step = sum(sum(row) for row in board)
            print(f"Step {i}: {rooks_in_step} rooks")

        # Hiển thị solution cuối cùng
        print("\nFinal solution:")
        for row in result_ac3['solution']:
            print(" ".join("R" if cell == 1 else "." for cell in row))
    else:
        print("No solution found!")
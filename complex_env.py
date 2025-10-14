import copy
import time
import random
from collections import deque

N = 8


class AndOrNode:
    def __init__(self, board, row=0, is_and=False, action=None):
        self.board = [r[:] for r in board]  # copy board
        self.row = row
        self.is_and = is_and
        self.action = action  # tuple (row, col) nếu AND node
        self.children = []


class AndOrSearch:
    def __init__(self, target_board=None):
        self.N = N
        self.target = target_board
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []

    def is_goal(self, board):
        """Kiểm tra xem board có phải là goal state không"""
        # Nếu có target board, so sánh với target
        if self.target is not None:
            return board == self.target

        # Nếu không có target, kiểm tra tiêu chuẩn 8 rooks
        rook_count = sum(sum(row) for row in board)
        if rook_count != self.N:
            return False

        for i in range(self.N):
            if sum(board[i]) != 1:
                return False
            if sum(board[j][i] for j in range(self.N)) != 1:
                return False
        return True

    def is_valid(self, board, row, col):
        """Kiểm tra việc đặt rook tại (row, col) có hợp lệ không"""
        # Kiểm tra cột
        for i in range(self.N):
            if board[i][col] == 1:
                return False
        # Kiểm tra hàng
        for j in range(self.N):
            if board[row][j] == 1:
                return False
        return True

    def get_valid_moves(self, board, row):
        """Lấy tất cả các nước đi hợp lệ cho hàng hiện tại"""
        valid_moves = []
        for col in range(self.N):
            if self.is_valid(board, row, col):
                valid_moves.append(col)
        return valid_moves

    def or_search(self, state, row, path):
        """Tìm kiếm OR node - chọn hành động cho hàng hiện tại"""
        self.nodes_expanded += 1
        self.solution_path.append(copy.deepcopy(state))

        # Kiểm tra goal
        if self.is_goal(state):
            return AndOrNode(state, row)

        # Kiểm tra đã xử lý hết các hàng
        if row >= self.N:
            return None

        state_tuple = tuple(tuple(r) for r in state)
        if state_tuple in path:
            return None

        path.add(state_tuple)
        or_node = AndOrNode(state, row)

        # Lấy các nước đi hợp lệ
        valid_moves = self.get_valid_moves(state, row)
        self.max_frontier_size = max(self.max_frontier_size, len(valid_moves))

        # Thử từng nước đi hợp lệ
        for col in valid_moves:
            new_state = copy.deepcopy(state)
            new_state[row][col] = 1

            # Gọi AND search cho hàng tiếp theo
            result = self.and_search(new_state, row + 1, path)
            if result is not None:
                # Tạo AND node cho hành động thành công
                and_node = AndOrNode(new_state, row, is_and=True, action=(row, col))
                and_node.children.append(result)
                or_node.children.append(and_node)
                path.remove(state_tuple)
                return or_node

        path.remove(state_tuple)
        return None

    def and_search(self, state, row, path):
        """Tìm kiếm AND node - xử lý trạng thái tiếp theo"""
        # Nếu đã xử lý hết các hàng, kiểm tra goal
        if row >= self.N:
            if self.is_goal(state):
                return AndOrNode(state, row)
            return None

        # Gọi OR search cho hàng hiện tại
        return self.or_search(state, row, path)

    def extract_solution_path(self, node):
        """Trích xuất đường đi solution từ cây"""
        if node is None:
            return []

        path = []
        current = node

        while current:
            path.append(current.board)
            if current.children:
                # Đi theo nhánh đầu tiên (solution)
                if current.is_and and current.children:
                    current = current.children[0]
                elif not current.is_and and current.children:
                    current = current.children[0].children[0] if current.children[0].children else None
                else:
                    break
            else:
                break

        return path

    def extract_solution_board(self, node):
        """Trích xuất board solution từ node"""
        if node is None:
            return None

        # Tìm node lá (goal state)
        if self.is_goal(node.board):
            return node.board

        for child in node.children:
            result = self.extract_solution_board(child)
            if result is not None:
                return result

        return None

    def solve_eight_rooks(self):
        """Giải bài toán Eight Rooks sử dụng AND-OR Search"""
        start_time = time.time()

        # Reset counters
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []

        # Tạo initial state
        initial_state = [[0] * self.N for _ in range(self.N)]
        path = set()

        # Thực hiện tìm kiếm
        solution_node = self.or_search(initial_state, 0, path)

        # Trích xuất kết quả
        solution_board = self.extract_solution_board(solution_node)

        # Nếu tìm thấy solution, trích xuất đường đi
        if solution_board is not None:
            self.solution_path = self.extract_solution_path(solution_node)
        else:
            self.solution_path = []

        end_time = time.time()

        return {
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size,
            "time": end_time - start_time,
            "path": self.solution_path,
            "solution": solution_board,
            "success": solution_board is not None
        }

    @staticmethod
    def solve_eight_rooks_static(target_board=None):
        """Static method để gọi từ UI - CÓ THỂ TRUYỀN TARGET BOARD"""
        solver = AndOrSearch(target_board)
        return solver.solve_eight_rooks()


# Wrapper function để gọi từ UI - CÓ THỂ TRUYỀN TARGET BOARD
def AND_OR_Search(target_board=None):
    return AndOrSearch.solve_eight_rooks_static(target_board)


class BeliefStateSearch:
    def __init__(self, target_board=None):
        self.N = N
        self.target = target_board
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []

    def is_goal_state(self, board):
        """Kiểm tra xem board có phải goal state không"""
        if self.target is not None:
            return board == self.target

        # Kiểm tra tiêu chuẩn
        rook_count = sum(sum(row) for row in board)
        if rook_count != self.N:
            return False

        for i in range(self.N):
            if sum(board[i]) != 1:
                return False
            if sum(board[j][i] for j in range(self.N)) != 1:
                return False
        return True

    def is_valid_move(self, board, row, col):
        """Kiểm tra nước đi hợp lệ"""
        # Kiểm tra cột
        for i in range(self.N):
            if board[i][col] == 1:
                return False
        # Kiểm tra hàng
        for j in range(self.N):
            if board[row][j] == 1:
                return False
        return True

    def get_possible_boards(self, belief_state):
        """Tạo tất cả các board có thể từ belief state hiện tại"""
        new_belief_state = []

        for board in belief_state:
            # Tìm hàng tiếp theo cần đặt rook (hàng đầu tiên chưa có rook)
            next_row = -1
            for row in range(self.N):
                if sum(board[row]) == 0:
                    next_row = row
                    break

            if next_row == -1:  # Đã đặt hết 8 rooks
                continue

            for col in range(self.N):
                if self.is_valid_move(board, next_row, col):
                    new_board = copy.deepcopy(board)
                    new_board[next_row][col] = 1
                    new_belief_state.append(new_board)

        return new_belief_state

    def belief_state_search(self):
        """Thuật toán Belief State Search - ĐÃ SỬA"""
        start_time = time.time()

        # Reset counters
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []

        # Khởi tạo belief state (chỉ có board rỗng)
        initial_belief = [[[0] * self.N for _ in range(self.N)]]
        self.solution_path.append(copy.deepcopy(initial_belief[0]))

        queue = deque([(initial_belief, [initial_belief[0]])])  # (belief_state, path)

        while queue:
            self.nodes_expanded += 1
            current_belief, current_path = queue.popleft()

            # Kiểm tra nếu belief state chứa goal state
            goal_found = False
            goal_board = None
            for board in current_belief:
                if self.is_goal_state(board):
                    goal_found = True
                    goal_board = board
                    break

            if goal_found:
                self.solution_path = current_path + [goal_board]
                end_time = time.time()
                return {
                    "nodes_expanded": self.nodes_expanded,
                    "max_frontier_size": self.max_frontier_size,
                    "time": end_time - start_time,
                    "path": self.solution_path,
                    "solution": goal_board,  # TRẢ VỀ TARGET BOARD
                    "success": True
                }

            # Tạo belief state mới
            new_belief = self.get_possible_boards(current_belief)

            if new_belief:
                # Lấy board đầu tiên để hiển thị
                display_board = new_belief[0]
                new_path = current_path + [display_board]
                queue.append((new_belief, new_path))

                # Cập nhật max frontier size
                self.max_frontier_size = max(self.max_frontier_size, len(queue))

            # Giới hạn để tránh infinite loop
            if self.nodes_expanded > 10000:
                break

        end_time = time.time()
        return {
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size,
            "time": end_time - start_time,
            "path": self.solution_path,
            "solution": None,
            "success": False
        }

    @staticmethod
    def solve_eight_rooks_static(target_board=None):
        """Static method để gọi từ UI"""
        solver = BeliefStateSearch(target_board)
        return solver.belief_state_search()


def Belief_State_Search(target_board=None):
    return BeliefStateSearch.solve_eight_rooks_static(target_board)


class PartiallyObservableSearch:
    def __init__(self, target_board=None):
        self.N = N
        self.target = target_board
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []
        self.observations = []

    def is_goal_state(self, board):
        """Kiểm tra goal state"""
        if self.target is not None:
            return board == self.target

        rook_count = sum(sum(row) for row in board)
        if rook_count != self.N:
            return False

        for i in range(self.N):
            if sum(board[i]) != 1:
                return False
            if sum(board[j][i] for j in range(self.N)) != 1:
                return False
        return True

    def make_observation(self, board, row, col):
        """Thực hiện quan sát - trả về True nếu có rook"""
        return board[row][col] == 1

    def update_knowledge(self, knowledge, row, col, observation):
        """Cập nhật knowledge base sau khi quan sát - ĐÃ SỬA"""
        new_knowledge = copy.deepcopy(knowledge)

        if observation:
            # Có rook tại (row, col)
            new_knowledge[row][col] = 1
            # Đánh dấu các ô cùng hàng/cột là không có rook
            for i in range(self.N):
                if i != col:
                    new_knowledge[row][i] = -1  # -1 = không có rook
                if i != row:
                    new_knowledge[i][col] = -1
        else:
            # Không có rook tại (row, col)
            new_knowledge[row][col] = -1

        return new_knowledge

    def get_safe_action(self, knowledge):
        """Tìm hành động an toàn tiếp theo - ĐÃ SỬA"""
        # Ưu tiên các ô có thể có rook (chưa bị loại trừ)
        for row in range(self.N):
            for col in range(self.N):
                if knowledge[row][col] == 0:  # Chưa biết
                    # Kiểm tra xem ô này có thể đặt rook không
                    row_has_rook = any(knowledge[row][c] == 1 for c in range(self.N))
                    col_has_rook = any(knowledge[r][col] == 1 for r in range(self.N))
                    if not row_has_rook and not col_has_rook:
                        return (row, col)
        return None

    def complete_solution(self, knowledge):
        """Hoàn thành solution từ knowledge base - HÀM MỚI"""
        board = [[0] * self.N for _ in range(self.N)]

        # Copy các rook đã biết
        for i in range(self.N):
            for j in range(self.N):
                if knowledge[i][j] == 1:
                    board[i][j] = 1

        # Điền các rook còn thiếu
        for row in range(self.N):
            if sum(board[row]) == 0:  # Hàng chưa có rook
                for col in range(self.N):
                    if knowledge[row][col] != -1:  # Ô không bị cấm
                        board[row][col] = 1
                        break

        return board

    def knowledge_to_board(self, knowledge):
        """Chuyển knowledge base thành board hiển thị"""
        board = [[0] * self.N for _ in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if knowledge[i][j] == 1:
                    board[i][j] = 1
        return board

    def partially_observable_search(self):
        """Thuật toán Partially Observable Search - ĐÃ SỬA"""
        start_time = time.time()

        # Reset counters
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.solution_path = []
        self.observations = []

        # Tạo target board nếu chưa có
        if self.target is None:
            self.target = [[0] * self.N for _ in range(self.N)]
            cols = list(range(self.N))
            random.shuffle(cols)
            for row in range(self.N):
                self.target[row][cols[row]] = 1

        # Khởi tạo knowledge base (0 = chưa biết)
        knowledge = [[0] * self.N for _ in range(self.N)]
        self.solution_path.append(self.knowledge_to_board(knowledge))

        # Thực hiện tìm kiếm
        max_steps = self.N * 3  # Tăng số bước tối đa
        for step in range(max_steps):
            self.nodes_expanded += 1

            # Tìm hành động an toàn
            action = self.get_safe_action(knowledge)
            if action is None:
                # Không còn hành động an toàn, hoàn thành solution
                completed_board = self.complete_solution(knowledge)
                self.solution_path.append(completed_board)
                break

            row, col = action

            # Thực hiện quan sát
            observation = self.make_observation(self.target, row, col)
            self.observations.append((action, observation))

            # Cập nhật knowledge
            knowledge = self.update_knowledge(knowledge, row, col, observation)

            # Thêm vào solution path
            self.solution_path.append(self.knowledge_to_board(knowledge))

            # Kiểm tra goal
            current_board = self.knowledge_to_board(knowledge)
            if self.is_goal_state(current_board):
                break

            # Cập nhật frontier size (số ô chưa biết)
            unknown_count = sum(row.count(0) for row in knowledge)
            self.max_frontier_size = max(self.max_frontier_size, unknown_count)

        # Đảm bảo có đủ 8 rooks - HÀM MỚI
        final_knowledge_board = self.knowledge_to_board(knowledge)
        rook_count = sum(sum(row) for row in final_knowledge_board)

        if rook_count < self.N:
            # Hoàn thành solution nếu thiếu rook
            completed_board = self.complete_solution(knowledge)
            self.solution_path.append(completed_board)
            final_board = completed_board
        else:
            final_board = final_knowledge_board

        end_time = time.time()

        return {
            "nodes_expanded": self.nodes_expanded,
            "max_frontier_size": self.max_frontier_size,
            "time": end_time - start_time,
            "path": self.solution_path,
            "solution": final_board,
            "success": self.is_goal_state(final_board),
            "observations": self.observations
        }

    @staticmethod
    def solve_eight_rooks_static(target_board=None):
        """Static method để gọi từ UI"""
        solver = PartiallyObservableSearch(target_board)
        return solver.partially_observable_search()


def Partially_Observable_Search(target_board=None):
    return PartiallyObservableSearch.solve_eight_rooks_static(target_board)


# Test code
if __name__ == "__main__":
    print("Testing Complex Environment Algorithms...")

    # Tạo target board cụ thể để test
    test_target = [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]
    ]

    # Test Belief State Search
    print("\n=== Belief State Search ===")
    result_belief = Belief_State_Search(test_target)
    print(f"Success: {result_belief['success']}")
    print(f"Nodes: {result_belief['nodes_expanded']}, Time: {result_belief['time']:.4f}s")
    if result_belief['success']:
        print("Solution matches target:", result_belief['solution'] == test_target)

    # Test Partially Observable Search
    print("\n=== Partially Observable Search ===")
    result_pos = Partially_Observable_Search(test_target)
    print(f"Success: {result_pos['success']}")
    print(f"Nodes: {result_pos['nodes_expanded']}, Time: {result_pos['time']:.4f}s")
    print(f"Observations made: {len(result_pos['observations'])}")
    if result_pos['success']:
        rook_count = sum(sum(row) for row in result_pos['solution'])
        print(f"Rooks in solution: {rook_count}/8")
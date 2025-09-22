import heapq
import queue
import random
import time

from UI import UI
N = 8

class Algorithm:
    #Tạo ma trận target
    @staticmethod
    def isvalid1(check,val):
        return not val in check

    @staticmethod
    def create_target():
        matrix = [[ 0 for _ in range(N)] for i in range(N)]
        check = []
        for i in range(N):
            while True:
                j = random.randint(0,N - 1)
                if Algorithm.isvalid1(check, j):
                    matrix[i][j] = 1
                    check.append(j)
                    break
        return matrix

    def bfs(self, target, window):
        canvas = UI.canvas_left(window)
        node = [[0]*N for i in range(8)]
        frontier = queue.Queue()
        frontier.put([node, 0])
        explored = set()
        while not frontier.empty():
            state, row = frontier.get()
            explored.add(tuple(map(tuple, state)))
            UI.drawtable(canvas, state)
            window.update()
            if row == N:
                if self.goal_test(state, target):
                    return state

            for i in range(N):
                if self.valid(state, row, i):
                    temp_state = self.copy_matrix(state)
                    temp_state[row][i] = 1
                    temp_tuple = tuple(map(tuple, temp_state))
                    if temp_tuple not in explored:
                        in_frontier = any(tuple(map(tuple, s)) == temp_tuple for s, _ in frontier.queue)
                        if not in_frontier:
                            frontier.put([temp_state, row+1])
        return None

    def dfs(self, target, window):
        canvas = UI.canvas_left(window)
        node = [[0]*N for i in range(8)]
        frontier = [(node, 0)]
        explored = set()
        while frontier:
            state, row = frontier.pop()
            explored.add(tuple(map(tuple, state)))
            UI.drawtable(canvas, state)
            window.update()
            if row == N:
                if self.goal_test(state, target):
                    return state
            for i in range(N):
                if self.valid(state, row, i):
                    temp_state = self.copy_matrix(state)
                    temp_state[row][i] = 1
                    temp_tuple = tuple(map(tuple, temp_state))
                    if temp_tuple not in explored:
                        in_frontier = any(tuple(map(tuple, s)) == temp_tuple for s, _ in frontier)
                        if not in_frontier:
                            frontier.append((temp_state, row+1))
        return None


    def dls(self, target, limit, window):
        node = [[0] * N for i in range(8)]
        return self.recursive_dls(node, target, limit, 0, window)

    def recursive_dls(self, state, target, limit, i, window, canvas=None):
        if canvas is None:
            canvas = UI.canvas_left(window)

        canvas.delete("all")
        UI.drawtable(canvas, state)
        window.update()
        time.sleep(0.5)

        if self.goal_test(state, target):
            return state
        elif limit == 0:
            return "cutoff"
        else:
            cutoff_occurred = False
            for j in range(N):
                if self.valid(state, i, j):
                    temp_state = self.copy_matrix(state)
                    temp_state[i][j] = 1
                    result = self.recursive_dls(temp_state, target, limit - 1, i + 1, window, canvas)
                    if result == "cutoff":
                        cutoff_occurred = True
                    elif result != "failure":
                        return result
            return "cutoff" if cutoff_occurred else "failure"

    def ucs(self, target, window):
        canvas = UI.canvas_left(window)
        node = [[0] * N for _ in range(N)]
        frontier = []
        heapq.heappush(frontier, (0, node, 0, []))
        explored = set()
        center = (N - 1) / 2
        while frontier:
            cost, state, row, path = heapq.heappop(frontier)
            explored.add(tuple(map(tuple, state)))
            UI.drawtable(canvas, state)
            window.update()
            if row == N and self.goal_test(state, target):
                print("Tìm thấy lời giải với chi phí:", cost)
                print("Đường đi:", path)
                return state
            if row < N:
                for i in range(N):
                    if self.valid(state, row, i):
                        temp_state = self.copy_matrix(state)
                        temp_state[row][i] = 1
                        temp_tuple = tuple(map(tuple, temp_state))
                        if temp_tuple not in explored:
                            # Chi phí
                            position_cost = abs(row - center) + abs(i - center) + 1
                            new_cost = cost + position_cost
                            new_path = path + [(row, i)]
                            heapq.heappush(frontier, (new_cost, temp_state, row + 1, new_path))
        return None

    def ids(self, target, window):
        for i in range(N):
            result = self.dls(target, i, window)
            if result != "cutoff":
                return  result
        return None
    @staticmethod
    def manhattan_heuristic(state, target):
        h = 0
        for i in range(N):
            col_state = None
            col_target = None
            for j in range(N):
                if state[i][j] == 1:
                    col_state = j
                    break
            for j in range(N):
                if target[i][j] == 1:
                    col_target = j
                    break
            if col_state is not None and col_target is not None:
                h += abs(col_state - col_target)
            elif col_state is None:
                #tăng chi phí khi chưa đặt
                h+= N
        return h

    def greedy_best_first(self, target, window):
        canvas = UI.canvas_left(window)
        node = [[0] * N for _ in range(N)]
        frontier = []
        heapq.heappush(frontier, (self.manhattan_heuristic(node, target), node, 0))
        explored = set()
        while frontier:
            h, state, row = heapq.heappop(frontier)
            explored.add(tuple(map(tuple, state)))
            canvas.delete("all")
            UI.drawtable(canvas, state)
            window.update()
            time.sleep(0.5)
            if row == N and self.goal_test(state, target):
                return state

            if row < N:
                for i in range(N):
                    if self.valid(state, row, i):
                        temp_state = self.copy_matrix(state)
                        temp_state[row][i] = 1
                        temp_tuple = tuple(map(tuple, temp_state))
                        if temp_tuple not in explored:
                            h_new = self.manhattan_heuristic(temp_state, target)
                            heapq.heappush(frontier, (h_new, temp_state, row + 1))
        return None

    def astar(self, target, window):
        canvas = UI.canvas_left(window)
        node = [[0] * N for _ in range(N)]
        start_h = self.manhattan_heuristic(node, target)

        # frontier: (f, g, state, row, path)
        frontier = []
        heapq.heappush(frontier, (start_h, 0, node, 0, []))
        explored = {}

        while frontier:
            f, g, state, row, path = heapq.heappop(frontier)
            state_tuple = tuple(map(tuple, state))

            # nếu đã duyệt trạng thái này với g nhỏ hơn thì bỏ qua
            if state_tuple in explored and explored[state_tuple] <= g:
                continue
            explored[state_tuple] = g

            canvas.delete("all")
            UI.drawtable(canvas, state)
            window.update()
            time.sleep(0.5)

            if row == N and self.goal_test(state, target):
                return state

            if row < N:
                for i in range(N):
                    if self.valid(state, row, i):
                        temp_state = self.copy_matrix(state)
                        temp_state[row][i] = 1
                        temp_tuple = tuple(map(tuple, temp_state))

                        g_new = g + 1  # mỗi bước đặt 1 quân = chi phí 1
                        h_new = self.manhattan_heuristic(temp_state, target)
                        f_new = g_new + h_new
                        new_path = path + [(row, i)]

                        heapq.heappush(frontier, (f_new, g_new, temp_state, row + 1, new_path))

        return None

    def goal_test(self, state, target):
        return state == target
    def copy_matrix(self, matrix):
        return [[matrix[i][j] for j in range(N)] for i in range(N)]
    def valid(self, matrix, row, col):
        for i in range(row):
            if matrix[i][col] == 1:
                return False
        return True






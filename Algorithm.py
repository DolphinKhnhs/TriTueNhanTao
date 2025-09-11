import random
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

    #Triển khai thuật toán DFS
    @staticmethod
    def dfs(target, window):
        init = [[0]*N for _ in range(N)]
        frontier = [(init, 0)]
        canvas = UI.canvas_left(window)
        explore = set()
        while frontier:
            state, row = frontier.pop()
            state_add = tuple(map(tuple, state))
            if state_add in explore:
                continue
            explore.add(state_add)
            if row == N and Algorithm.goal(state, target):
                return state
            for col in range(N):
                if Algorithm.isvalid2(row, col, state):
                    temp_state = Algorithm.copy_matrix(state)
                    temp_state[row][col] = 1
                    child = tuple(map(tuple,temp_state))
                    UI.drawtable(canvas, temp_state)
                    window.update()
                    window.after(1)
                    if child not in explore and all(tuple(map(tuple,s[0])) != child for s in frontier):
                        frontier.append((temp_state, row + 1))
        return None

    @staticmethod
    def goal(matrix, target):
        for i in range(N):
            for j in range(N):
                if matrix[i][j] != target[i][j]:
                    return False
        return True
    @staticmethod
    def isvalid2(row, col, state):
        for i in range(row):
            if state[i][col] == 1:
                return False
        return True
    @staticmethod
    def copy_matrix(matrix):
        return [row[:] for row in matrix]











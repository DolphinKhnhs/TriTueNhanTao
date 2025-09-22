import random

N = 8

def isvalid1(check, val):
    return val not in check

class Create:
    def __init__(self):
        self.size = N
        self.matrix = [[0 for _ in range(N)] for _ in range(N)]
        self.check = []

    def target(self):
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.check = []
        for i in range(self.size):
            while True:
                j = random.randint(0, self.size - 1)
                if isvalid1(self.check, j):
                    self.matrix[i][j] = 1
                    self.check.append(j)
                    break
        return self.matrix



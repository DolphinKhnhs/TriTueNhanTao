import math

N = 8

def cost(row, col, N):
    remove = 2 * (N - 1)
    center = (N - 1) / 2
    dist = abs(row - center) + abs(col - center)
    return remove + ((N - 1) * 2 - dist)


a = [[cost(i, j, N) for j in range(N)] for i in range(N)]

for row in a:
    print(row)

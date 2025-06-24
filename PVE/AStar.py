import numpy as np
from numba import njit, prange
import heapq

@njit
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

@njit
def neighbors(pos, rows, cols):
    x, y = pos
    result = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            result.append((nx, ny))
    return result


def a_star(grid, start, goal):
    rows, cols = grid.shape
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        x, y = current
        nbrs = get_valid_neighbors(x, y, grid)

        for neighbor in nbrs:
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None

@njit(parallel=True)
def get_valid_neighbors(x, y, grid):
    rows, cols = grid.shape
    result = []

    for i in prange(4):
        dx = np.array([-1, 1, 0, 0])[i]
        dy = np.array([0, 0, -1, 1])[i]
        nx = x + dx
        ny = y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx, ny] == 0:
                result.append((nx, ny))

    return result

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

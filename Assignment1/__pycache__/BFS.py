import maze
import numpy
from queue import Queue

EMPTY = 0
FILLED = 1

bfs_maze = maze.Maze(dim = 10, p = 0.3)


def neighbors(x, y, dim): # given x,y,dim,return the list of its neighbors
    result = []
    if x > 0:
        result.append((x-1, y))

    if y > 0:
        result.append((x, y-1))

    if x < dim-1:
        result.append((x+1, y))

    if y < dim-1:
        result.append((x, y+1))

    return result

def BFS(bfs_maze: maze.Maze):
    
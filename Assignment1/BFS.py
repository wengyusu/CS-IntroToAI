import maze
import numpy
from queue import Queue

EMPTY = 0
FILLED = 1

bfs_maze = maze.Maze(dim = 10, p = 0.3)

class Cell(object):
    def __init__(self, position, pre = None):
        self.position = position
        self.pre = pre

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
    bfs_maze.print_maze()
    queue = Queue()
    path = []
    start = (0,0)
    queue.put(Cell(start))
    visited = numpy.zeros((bfs_maze.dim, bfs_maze.dim)) # create a matrix to mark whether the cell was visited
    visited[0, 0] = 1
    while queue.empty() is False:
        cell = queue.get()
        # print(cell.position)
        if cell.position == (bfs_maze.dim-1, bfs_maze.dim-1):
            print("Find a solution")
            pre_cell = cell.pre
            path.append((bfs_maze.dim-1, bfs_maze.dim-1))
            while pre_cell is not None:
                # print(pre_cell.position)
                path.append(pre_cell.position)
                pre_cell = pre_cell.pre

            for node in reversed(path):
                print(node)
            break

        for neighbor in neighbors(cell.position[0], cell.position[1], bfs_maze.dim):
            if visited[neighbor[0], neighbor[1]] != 1 and bfs_maze.maze[neighbor[0], neighbor[1]] == EMPTY:
                visited[neighbor[0], neighbor[1]] = 1
                next_cell = Cell(position = neighbor, pre = cell)
                queue.put(next_cell)
                # break
        
if __name__ == "__main__":
    BFS(bfs_maze)
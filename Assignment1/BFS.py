import maze
import numpy
from queue import Queue

EMPTY = 0
FILLED = 1



class Cell(object):
    def __init__(self, position, pre = None):
        self.position = position
        self.pre = pre
        

class BFS(object):

    def __init__(self, maze:maze.Maze):
        self.maze = maze
        self.queue = Queue()
        self.path = []

    def neighbors(self, x, y, dim): # given x,y,dim,return the list of its neighbors
        result = []
        if x < dim-1:
            result.append((x+1, y))

        if y < dim-1:
            result.append((x, y+1))

        if x > 0:
            result.append((x-1, y))

        if y > 0:
            result.append((x, y-1))

        return result

    def search(self):
        # bfs_maze.print_maze()
        start = (0,0)
        self.queue.put(Cell(start))
        visited = numpy.zeros((self.maze.dim, self.maze.dim)) # create a matrix to mark whether the cell was visited
        visited[0, 0] = 1
        while self.queue.empty() is False:
            cell = self.queue.get()
            # print(cell.position)
            if cell.position == (self.maze.dim-1, self.maze.dim-1):
                # print("Find a solution")
                pre_cell = cell.pre
                self.path.append((self.maze.dim-1, self.maze.dim-1))
                while pre_cell is not None:
                    # print(pre_cell.position)
                    self.path.append(pre_cell.position)
                    pre_cell = pre_cell.pre

                self.path = self.path[::-1]
                    # print(node)
                return True

            for neighbor in self.neighbors(cell.position[0], cell.position[1], self.maze.dim):
                if visited[neighbor[0], neighbor[1]] != 1 and self.maze.maze[neighbor[0], neighbor[1]] == EMPTY:
                    visited[neighbor[0], neighbor[1]] = 1
                    next_cell = Cell(position = neighbor, pre = cell)
                    self.queue.put(next_cell)
                    # break
        return False
        
if __name__ == "__main__":
    bfs_maze = maze.Maze(dim = 10, p = 0.2)
    bfs_maze.print_maze()
    bfs = BFS(bfs_maze)
    bfs.search()
    if bfs.path :
        print("Find a path", bfs.path)
    else:
        print("cannot find a path")
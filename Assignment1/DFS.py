import maze
import numpy
import time

EMPTY = 0
FILLED = 1

class Cell(object):
    def __init__(self, position, pre = None):
        self.position = position
        self.pre = pre

class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self, value):  
        self.stack.append(value)

    def pop(self):  
        if self.stack:
            self.stack.pop()
        else:
            raise LookupError('stack is empty!')

    def is_empty(self): 
        return not bool(self.stack)

    def top(self): 
        return self.stack[-1]


class DFS(object):

    def __init__(self, maze):
        self.maze = maze
        self.stack = Stack()
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
        # dfs_maze.print_maze()
        self.stack.push(Cell((0,0)))
        visited = numpy.zeros((self.maze.dim, self.maze.dim)) # create a matrix to mark whether the cell was visited
        visited[0,0] = 1
        while self.stack.is_empty() is False:
            cell = self.stack.top()
            self.stack.pop()
            # print(cell.position)
            # if cell.pre is not None:
            # print(cell.position)
            # visited[cell.position] = 1
            if cell.position == (self.maze.dim-1, self.maze.dim-1):
                # print(self.stack.stack)
                pre_cell = cell.pre
                self.path.append((self.maze.dim-1, self.maze.dim-1))
                while pre_cell is not None:
                    # print(pre_cell.position)
                    self.path.append(pre_cell.position)
                    pre_cell = pre_cell.pre

                self.path = self.path[::-1]
                return True
            for neighbor in self.neighbors(cell.position[0], cell.position[1], self.maze.dim):
                if visited[neighbor] != 1 and self.maze.maze[neighbor] == EMPTY:
                    # print(neighbor)
                    visited[neighbor] = 1
                    next_cell = Cell(position = neighbor, pre = cell)
                    self.stack.push(next_cell)

        return False

if  __name__ == "__main__":
    dfs_maze = maze.Maze(dim = 10, p = 0.2)
    start = time.time()
    dfs_maze.print_maze()
    dfs = DFS(dfs_maze)
    dfs.search()
    if dfs.path :
        print("Find a path", dfs.path)
    else:
        print("cannot find a path")
    end = time.time()
    print(end - start)
  

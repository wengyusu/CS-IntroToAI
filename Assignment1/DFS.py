import maze
import numpy

EMPTY = 0
FILLED = 1

dfs_maze = maze.Maze(dim = 10, p = 0.3)

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
        return bool(self.stack) or self.stack == []

    def top(self): 
        return self.stack[-1]

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

def dfs(dfs_maze: maze.Maze):
    dfs_maze.print_maze()
    stack = Stack()
    stack.push((0,0))
    visited = numpy.zeros((dfs_maze.dim, dfs_maze.dim)) # create a matrix to mark whether the cell was visited
    # visited[0, 0] = 1
    while stack.is_empty is False:
        cell = stack.top()
        # print(cell)
        if cell == (dfs_maze.dim-1, dfs_maze.dim-1):
            print(stack.stack)
            break
        for neighbor in neighbors(cell[0], cell[1], dfs_maze.dim):
            if visited[neighbor[0], neighbor[1]] != 1 and dfs_maze.maze[neighbor[0], neighbor[1]] == EMPTY:
                stack.push(neighbor)
                visited[neighbor[0], neighbor[1]] = 1
                break
        
        else:
            visited[cell[0], cell[1]] = 1
            stack.pop()

if  __name__ == "__main__":
    dfs(dfs_maze)
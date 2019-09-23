import maze as mazepkg
import numpy

EMPTY = 0
FILLED = 1




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
    def len(self):
        return len(self.stack)
class DFS:
    def __init__(self,dim,p):
        self.dim=dim
        self.p=p
        self.maze = mazepkg.Maze(dim=dim, p=p)
        self.maze.print_maze()
        self.fringe=0
        self.dfs(self.maze)





    def neighbors(self,x, y, dim):  # given x,y,dim,return the list of its neighbors
        result = []
        if x > 0:
            result.append((x - 1, y))

        if y > 0:
            result.append((x, y - 1))

        if x < dim - 1:
            result.append((x + 1, y))

        if y < dim - 1:
            result.append((x, y + 1))

        return result


    def dfs(self,dfs_maze: mazepkg.Maze):
        stack = Stack()
        stack.push((0, 0))

        visited = numpy.zeros((dfs_maze.dim, dfs_maze.dim))  # create a matrix to mark whether the cell was visited
        # visited[0, 0] = 1
        while stack.is_empty is False:
            self.fringe = max(stack.len(), self.fringe)
            cell = stack.top()
            # print(cell)
            if cell == (dfs_maze.dim - 1, dfs_maze.dim - 1):
                print(stack.stack)
                break
            for neighbor in self.neighbors(cell[0], cell[1], dfs_maze.dim):
                if visited[neighbor[0], neighbor[1]] != 1 and dfs_maze.maze[neighbor[0], neighbor[1]] == EMPTY:
                    stack.push(neighbor)
                    visited[neighbor[0], neighbor[1]] = 1
                    break

            else:
                visited[cell[0], cell[1]] = 1
                stack.pop()


if __name__ == "__main__":
    dfs=DFS(10,0.2)
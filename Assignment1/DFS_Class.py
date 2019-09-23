import maze as mazepkg
import numpy

EMPTY = 0
FILLED = 1

class DFS:
    def __init__(self,dim,p):
        self.dim=dim
        self.p=p
        self.maze = mazepkg.Maze(dim=dim, p=p)
        self.maze.print_maze()
        self.fringe=0
        self.dfs()
        type(self.maze)





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


    def dfs(self):
        stack =[]
        stack.append((0,0))
        visited=[[0]*self.dim for i in range(self.dim)]
        visited[0][0]=1
        path={}
        while (len(stack)!=0):
            cell=stack.pop()
        for neigbor  in self.neighbors(cell[0],cell[1],self.dim):
            if self.maze[neigbor[1]][neigbor[0]]!=FILLED and visited[neigbor[1]][neigbor[0]] !=1:
                stack.append(neigbor)
                visited[neigbor[1]][neigbor[0]] = 1
                path[neigbor]=cell







if __name__ == "__main__":
    dfs=DFS(10,0.2)

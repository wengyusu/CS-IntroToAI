import maze as mazepkg

import numpy

EMPTY = 0
FILLED = 1
PATH=100
class DFS:
    def __init__(self,dim,p):
        self.maze_object = mazepkg.Maze(dim=dim, p=p)
        self.dim=dim
        self.p=p

        self.maze_object.print_maze()
        self.maze=self.maze_object.maze

        self.fringe_size=0
        self.dfs()
        # type(self.maze)





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
        self.path={}
        while (len(stack)!=0):
            self.fringe_size=max(self.fringe_size,len(stack))
            cell=stack.pop()
            if(cell[0]==self.dim-1 and cell[1]==self.dim-1):
                return True
            for neigbor  in self.neighbors(cell[0],cell[1],self.dim):
                if self.maze[neigbor[1]][neigbor[0]]!=FILLED and visited[neigbor[1]][neigbor[0]] !=1:
                    stack.append(neigbor)
                    visited[neigbor[1]][neigbor[0]] = 1
                    self.path[neigbor]=cell
        return False

    def calculate_path(self):
        current = (self.dim-1, self.dim-1)
        if current not in self.path:
            print("no path found")
            return False
        while current != (0, 0):
            self.maze[current[1]][current[0]] = PATH
            current = self.path[current]
        self.maze[0][0] = PATH
        return True

    def print_final_maze(self):
        print(numpy.matrix(self.maze))

    def get_fringe_size(self):
        if self.solvable():
            print ("fring size max is {}".format(self.fringe_size))
            return  self.fringe_size
        print("no path found")

    def print_original_maze(self):
        print(numpy.matrix(self.maze))

    def solvable(self):
        return  self.dfs()



if __name__ == "__main__":
    dfs=DFS(10,0.2)
    dfs.get_fringe_size()

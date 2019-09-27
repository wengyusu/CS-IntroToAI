import DFS
import maze
import numpy

class Improved_DFS(DFS.DFS):
    def neighbors(self, x, y, dim): # given x,y,dim,return the list of its neighbors
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

if __name__ == "__main__":
    # m = maze.Maze(10,0.2)
    # dfs = Improved_DFS(m)
    # dfs.search()  
    # print(dfs.path)
    print("Test avg length between traditional DFS and improved one:")
    length = 0
    num = 0
    for i in range(1000):
        m = maze.Maze(128, 0.2)
        dfs = DFS.DFS(m)
        dfs.search()
        # print(len(dfs.path))
        if len(dfs.path) != 0:
            length = length + len(dfs.path)
            num = num +1
    print("Avg len of traditional DFS: {}".format(length/num))
    length = 0
    num = 0
    for i in range(1000):
        m = maze.Maze(128, 0.2)
        dfs = Improved_DFS(m)
        dfs.search()
        # print(len(dfs.path))
        if len(dfs.path) != 0:
            length = length + len(dfs.path)
            num = num +1
    print("Avg len of Improved DFS: {}".format(length/num))
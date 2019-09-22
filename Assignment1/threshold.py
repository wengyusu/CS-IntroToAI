import DFS
import maze

p_list = range(1, 20)
dim = 512

for p in p_list:
    p= p/100
    solv = 0
    for i in range(0, 1000):
        m = maze.Maze(dim = 512, p = p)
        if DFS.dfs(m):
            solv = solv +1

    print("when p = {}, the probability that the maze is solvable is: {}".format(p, solv/1000))
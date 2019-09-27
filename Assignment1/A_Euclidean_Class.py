import maze as mazepkg
import numpy
import math
import heapq


PATH=100
class A_Euclidean:
    def __init__(self,dim,p):
        self.node_visited = None
        self.dim=dim
        self.p=p
        maze_object = mazepkg.Maze(dim=self.dim, p=self.p)
        self.maze = maze_object.maze
        self.print_original_maze()
        self.runMaze()


    def runMaze(self):
        self.trace_back()
        self.calculate_path()

    def print_original_maze(self):
        print(numpy.matrix(self.maze))




    def get_node_visited(self):
        if self.node_visited!=None:
            print("Node visited is {}".format(self.node_visited))
            return  self.node_visited
    def get_path_length(self):
        print("Path length is {}".format(self.path_length))
        return self.path_length

    def generate_EuclideanDistance(self):
        '''
        set heuristic "h"
        suppose coorX is len(maze)
        suppose coorY is len(maze[0])
        maze[y][x]
        '''
        sizeY = len(self.maze)
        sizeX = len(self.maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1
        distance_Euclidean = [[0] * sizeX for i in range(sizeY)]
        for x in range(sizeX):
            for y in range(sizeY):
                distance_Euclidean[x][y] = math.sqrt(((max_coorX - x) ** 2 + (max_coorY - y) ** 2))
        distance_Euclidean[0][0] = 0
        return distance_Euclidean


    def neighbour(self,node):
        '''
        return a list of tuple with (coorY,coorX)
        which was not filled(obstacle)
        and is the neighbour of the curent one
        :param node（coor_y,coor_x）:
        :param maze:
        :return:
        '''
        neighbour_node = []
        coor_x = node[1]
        coor_y = node[0]
        sizeY = len(self.maze)
        sizeX = len(self.maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1

        if coor_x > 0:
            x_minus_one = coor_x - 1
            letf_one = (coor_y, x_minus_one)
            if (self.maze[coor_y][x_minus_one]) == 0:
                neighbour_node.append(letf_one)

        if coor_x < max_coorX:
            x_plus_one = coor_x + 1
            right_one = (coor_y, x_plus_one)
            if (self.maze[coor_y][x_plus_one]) == 0:
                neighbour_node.append(right_one)

        if coor_y > 0:
            y_minus_one = coor_y - 1
            below_one = (y_minus_one, coor_x)
            if (self.maze[y_minus_one][coor_x]) == 0:
                neighbour_node.append(below_one)

        if coor_y < max_coorY:
            y_plus_one = coor_y + 1
            above_one = (y_plus_one, coor_x)
            if (self.maze[y_plus_one][coor_x]) == 0:
                neighbour_node.append(above_one)
        return neighbour_node


    def generate_path(self):
        '''
        using 2d list track the previous node
        :param maze:
        :return:
        '''
        sizeY = len(self.maze)
        sizeX = len(self.maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1
        distanceE = self.generate_EuclideanDistance()
        pq = []
        path = {}
        visited = [[False] * sizeX for i in range(sizeY)]
        costed = [[0] * sizeX for i in range(sizeY)]
        heapq.heappush(pq, (0, (0, 0)))
        visited[0][0] = True
        while len(pq) != 0:
            node = heapq.heappop(pq)[1]
            if node == (max_coorX, max_coorY):
                self.node_visited=numpy.sum(visited )

                break
            for (coor_y, coor_x) in self.neighbour(node):
                if not visited[coor_y][coor_x]:
                    costed[coor_y][coor_x] = costed[node[0]][node[1]] + 1
                    visited[coor_y][coor_x] = True
                    heapq.heappush(pq, (costed[coor_y][coor_x] + distanceE[coor_y][coor_x], (coor_y, coor_x)))
                    path[(coor_y, coor_x)] = (node[0], node[1])
        return path


    def trace_back(self):
        '''
        print the path when existed
        :param maze:
        :return:
        '''
        path= self.generate_path()
        sizeY = len(self.maze)
        sizeX = len(self.maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1
        current = (max_coorY, max_coorX)
        if current not in path:
            print("no path found")
            return False
        while current != (0, 0):
            self.maze[current[0]][current[1]] = PATH
            current = path[current]
        self.maze[0][0] = PATH
        return True



    def calculate_path (self):
        '''

        :param maze: a maze which is path found maze, which mean 0 represent empty 1 represent filled 100 represent path
        :return: total path length
        '''

        path_length=numpy.sum(self.maze==PATH)
        # print("total path length is {}".format(path_length))
        self.path_length=path_length
        return path_length
    def print_final_path(self):
        '''

        :param maze: a maze generated randomly
        :return: print original maze and path-found maze(100 represent "Path")
        '''


        print(numpy.matrix(self.maze))



if __name__ == "__main__":
    a=A_Euclidean(dim=10,p=0.3)

    a.get_path_length()
    a.get_node_visited()
    a.print_final_path()
    #print original maze and path-found maze(100 represent "Path")









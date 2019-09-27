import maze
import numpy
import math
import heapq
import BFS
from queue import PriorityQueue

PATH=100
EMPTY = 0
FILLED = 1
FIRE = -1
class A_star(object):

    def __init__(self, maze):
        self.maze = maze
        self.path_length = None
        self.path = []

    def generate_EuclideanDistance(self):
        '''
        set heuristic "h"
        suppose coorX is len(maze)
        suppose coorY is len(maze[0])
        maze[y][x]
        '''
        sizeY=len(self.maze)
        sizeX=len(self.maze[0])
        max_coorY=sizeY-1
        max_coorX=sizeX-1
        distance_Euclidean=[[0] * sizeX for i in range(sizeY)]
        for x in range(sizeX):
            for y in range(sizeY):
                distance_Euclidean[x][y]=math.sqrt(((max_coorX-x)**2+(max_coorY-y)**2))
        distance_Euclidean[0][0]=0
        return distance_Euclidean

    def neighbour(self, node):
        '''
        return a list of tuple with (coorY,coorX)
        which was not filled(obstacle)
        and is the neighbour of the curent one
        :param node:
        :param maze:
        :return:
        '''
        neighbour_node=[]
        coor_x=node[1]
        coor_y=node[0]
        sizeY=len(self.maze)
        sizeX=len(self.maze[0])
        max_coorY=sizeY-1
        max_coorX=sizeX-1

        if coor_x>0:
            x_minus_one = coor_x - 1
            letf_one = (coor_y, x_minus_one)
            if (self.maze[coor_y][x_minus_one]) == 0:
                neighbour_node.append(letf_one)

        if coor_x<max_coorX:
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
        pq=[]
        path={}
        visited=[[False]*sizeX for i in range(sizeY)]
        costed= [[0] * sizeX for i in range(sizeY)]
        heapq.heappush(pq,(0,(0,0)))
        visited[0][0]=True
        while len(pq)!=0:
            node=heapq.heappop(pq)[1]
            if node==(max_coorX,max_coorY):
                # print("find path")
                break
            for (coor_y,coor_x) in self.neighbour(node):
                if not visited[coor_y][coor_x]:
                    costed[coor_y][coor_x]=costed[node[0]][node[1]]+1
                    visited[coor_y][coor_x]=True
                    heapq.heappush(pq,(visited[coor_y][coor_x]+distanceE[coor_y][coor_x],(coor_y,coor_x)))
                    path[(coor_y,coor_x)]=(node[0],node[1])
        return path
    def trace_back(self):
        '''
        print the path when existed
        :param maze:
        :return:
        '''
        path=self.generate_path()
        sizeY = len(self.maze)
        sizeX = len(self.maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1
        current=(max_coorY,max_coorX)
        if current not in path:
            # print("no path found")
            return
        while current!=(0,0):
            self.maze[current[0]][current[1]]=PATH
            self.path.append(current)
            current=path[current]
        self.maze[0][0]=PATH
        # print(numpy.matrix(maze))
        return True

    def calculate_path (self):
        '''
        :param maze: a maze which is path found maze, which mean 0 represent empty 1 represent filled 100 represent path
        :return:  total path
        '''
        path_length=numpy.sum(self.maze==PATH)
        self.path_length = path_length
        # print("total path length is {}".format(path_length))
        
    def print_path(self):
        '''
        :param maze:  a maze generated randomly
        :return: print original maze and path-found maze(100 represent "Path")
        '''
        # print(numpy.matrix(self.maze))
        self.trace_back()
        # print(numpy.matrix(self.maze))
        self.calculate_path()
 
class Dijkstra(object):
    def __init__(self, maze: maze.Maze, start):
        self.maze = maze
        self.frontier = PriorityQueue()
        self.visited = {}
        self.cost = numpy.zeros((self.maze.dim, self.maze.dim))
        self.start = start
        self.frontier.put((0, self.start))
        self.visited[start] = None
        self.cost[self.start] = 0

    def neighbors(self, x, y): # given x,y,return the list of its neighbors
        result = []
        if x > 0:
            result.append((x-1, y))

        if y > 0:
            result.append((x, y-1))

        if x < self.maze.dim-1:
            result.append((x+1, y))

        if y < self.maze.dim-1:
            result.append((x, y+1))

        return result

    def cal_cost(self):
        # self.maze.print_maze()
        while not self.frontier.empty():
            current = self.frontier.get()[1]
            if current == (self.maze.dim-1, 0):
                break
            for cell in self.neighbors(current[0], current[1]):
                # print(cell)
                new_cost = self.cost[current[0], current[1]] + 1
                if self.maze.maze[cell[0], cell[1]] != FILLED and (self.cost[cell[0], cell[1]] == 0 or new_cost < self.cost[cell[0], cell[1]]):
                    self.cost[cell] = new_cost
                    priority = new_cost
                    self.frontier.put((priority, cell))
                    # print(cell)
                    self.visited[cell] = current

        self.cost[self.start] = 0
        # print(numpy.matrix(self.cost))
        return numpy.matrix(self.cost)

class BFS_Improved(BFS.BFS):
    def __init__(self, maze):
        super().__init__(maze)
        self.dis_from_fire = Dijkstra(self.maze, (0,self.maze.dim - 1)).cal_cost()
        self.cost = Dijkstra(self.maze, (0,0)).cal_cost()

    def search(self): 
        # self.maze.print_maze()
        start = (0,0)
        self.queue.put(BFS.Cell(start))
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

                # self.path = self.path[::-1]
                # print(self.path)
                    # print(node)
                return True

            for neighbor in self.neighbors(cell.position[0], cell.position[1], self.maze.dim):
                # new_cost = self.cost[cell.position] + 1
                # # print(new_cost)
                # if self.cost[neighbor] == 0 or new_cost < self.cost[neighbor]:
                #     self.cost[neighbor] = new_cost
                if visited[neighbor[0], neighbor[1]] != 1 and self.maze.maze[neighbor[0], neighbor[1]] == EMPTY and self.cost[neighbor] < self.dis_from_fire[neighbor]:
                    visited[neighbor[0], neighbor[1]] = 1
                    next_cell = BFS.Cell(position = neighbor, pre = cell)
                    self.queue.put(next_cell)
                    # break
        return False


class Astar_Improved(object):
    def __init__(self, maze):
        self.maze = maze
        self.frontier = PriorityQueue()
        self.visited = {}
        self.cost = numpy.zeros((self.maze.dim, self.maze.dim))
        # self.cost = Dijkstra(self.maze, (0,0)).cal_cost()
        self.dis_from_fire = Dijkstra(self.maze, (0, self.maze.dim - 1)).cal_cost()
        start = (0, 0)
        self.cost[start] = 0
        self.frontier.put((0, start))
        self.visited[start] = None
        # self.cost[start] = 0
        self.path = None
        self.path_length = None
        # if self.dis_from_fire[0, 0] != 0:
        self.dis = numpy.zeros((self.maze.dim, self.maze.dim))
        self.dis[0,0] = (self.maze.dim * self.maze.dim - self.dis_from_fire[0,0])/(2*self.maze.dim - 1)

    def neighbors(self, x, y): # given x,y,return the list of its neighbors
        result = []
        if x > 0:
            result.append((x-1, y))

        if y > 0:
            result.append((x, y-1))

        if x < self.maze.dim-1:
            result.append((x+1, y))

        if y < self.maze.dim-1:
            result.append((x, y+1))

        return result

    def search(self):
        # t = BFS_Improved(self.maze)
        # t.search()
        # if t.path or t.path != []:
        #     self.path = t.path
        #     self.path_length = len(self.path)
        #     return
        # self.maze.print_maze()
        while not self.frontier.empty():
            current = self.frontier.get()[1]
            # print(current)
            if current == (self.maze.dim-1, self.maze.dim-1):
                self.path = []
                while current != (0,0):
                    self.path.append(current)
                    # print(current)
                    current = self.visited[current]
                self.path.append((0,0))
                self.path_length = len(self.path)
                # print(self.path)
                break
            for cell in self.neighbors(current[0], current[1]):
                if self.maze.maze[cell[0], cell[1]] == EMPTY and cell != (0,0):
                    new_cost = self.cost[current] + 1
                    # if new_cost - self.dis_from_fire[cell[0], cell[1]] <= 0:
                    #     delta = self.dis[current]
                    # else:
                    delta = new_cost - self.dis_from_fire[cell[0], cell[1]]
                    new_dis = self.dis[current] + (self.maze.dim * self.maze.dim + delta) / (2*self.maze.dim - 1)
                    # delta = self.cost[cell] - self.dis_from_fire[cell[0], cell[1]]
                    # print(self.dis_from_fire[current[0], current[1]])
                    if self.cost[cell] == 0 or new_dis < self.dis[cell]:
                        self.cost[cell] = new_cost
                        # priority = new_cost + self.heuristic((self.maze.dim-1,self.maze.dim-1), cell)
                        # if delta < 0:
                        #     priority = -1
                        # else: 
                            # priority = new_cost + delta / (2*self.maze.dim -1 )
                        priority = delta
                        self.frontier.put((priority, cell))
                        self.visited[cell] = current
        # print(numpy.matrix(self.cost))  
        # print(numpy.matrix(self.maze.maze))

        # print(self.dis_from_fire[0, 0])
        

class Fire_maze(maze.Maze):
    def __init__(self, dim, p, q):
        super().__init__(dim, p)
        self.q = q
        self.maze[0, dim-1] = FIRE
        self.fire_list = set() # record cells which are on fire
        self.fire_list.add((0, dim-1))

    def neighbors(self, x, y): # given x,y,return the list of its neighbors
        result = []

        if x > 0:
            result.append((x-1, y))

        if y > 0:
            result.append((x, y-1))

        if x < self.dim-1:
            result.append((x+1, y))

        if y < self.dim-1:
            result.append((x, y+1))

        return result

    def fire_spread(self):
        confirm_list = set() # nodes that confirmed be on fire this time
        check_list = set() # nodes that may be on fire this time
        for node in self.fire_list:
            for neighbor in self.neighbors(node[0], node[1]):
                if self.maze[neighbor[0], neighbor[1]] == EMPTY or self.maze[neighbor[0], neighbor[1]] == PATH:
                    check_list.add(neighbor)

        for cell in check_list:
            x = cell[0]
            y = cell[1]
            fire_num = 0 # the num of neighbors on fire
            for neighbor in self.neighbors(x, y):
                if self.maze[neighbor[0], neighbor[1]] == FIRE:
                    fire_num = fire_num + 1
                p = (1-self.q)**fire_num
                if fire_num > 0 and self.probability(1-p):
                    confirm_list.add((x, y))
        
        # self.fire_list = []
        # print(confirm_list)/
        for i in confirm_list:
            self.fire_list.add(i)
            self.maze[i[0], i[1]] = FIRE


def test_rate(f_maze):
    # f_maze = Fire_maze(64, p, q)
    # f_maze.print_maze()
    search = BFS.BFS(f_maze)
    search.search()

    path = search.path[::-1]
    if search.path:
        # print(len(path))
        find = False
        for t in range(len(path)):
            # print(t)
            f_maze.fire_spread()
            if not path:
                break
            next_cell = path.pop()
            for p in path:
                if f_maze.maze[p[0], p[1]] == FIRE: # Find the path is unavaliable
                    find = True
                    break
            else:
                continue
            # print("The path is unavailable due to the fire")
            if find:
                return -1
        # print(numpy.matrix(f_maze.maze))
        return 1
    else:
        return 0 # the maze doesn't have a path

def test_improved_rate(f_maze):
    # f_maze = Fire_maze(64, p, q)
    # f_maze.print_maze()
    test = BFS.BFS(f_maze)
    test.search()
    search = Astar_Improved(f_maze)
    search.search()
    # search.print_path()
    # print(search.path)
    path = search.path
    if search.path:
        find = False
        for t in range(search.path_length):
            # print(t)
            f_maze.fire_spread()
            if not path:
                break
            next_cell = path.pop()
            for p in path:
                if f_maze.maze[p[0], p[1]] == FIRE:
                    find = True
                    break
            else:
                continue
            # print("The path is unavailable due to the fire")
            if find:
                return -1
            # print(numpy.matrix(f_maze.maze))
            # break
        # print(numpy.matrix(f_maze.maze))
        return 1
    else:
        if test.path:
            return -1
        return 0

def main(p):
    print("Show a sample:")
    test_maze = Fire_maze(10, 0.2, 0.5)
    test = Astar_Improved(test_maze)
    test.search()
    find = False
    if test.path:
        print(numpy.matrix(test.maze.maze))
        print(test.path)
        for t in range(test.path_length):
            test_maze.fire_spread()
            next_cell = test.path.pop()
            test_maze.maze[next_cell] = PATH
            for cell in test.path:
                if test_maze.maze[cell] == FIRE:
                    find = True
                    break
        if find:
            print("The path is unavailable due to the fire")
        print(numpy.matrix(test_maze.maze))

    for q in range(11):
        q = q/10
        Postive0 = 0
        Negative0 = 0
        Postive1 = 0
        Negative1 = 0
        for i in range(1000):
            f_maze = Fire_maze(32, p, q)
            res0 = test_improved_rate(f_maze)
            if  res0 == 1:
                Postive0 = Postive0 + 1
            elif res0 == -1:
                Negative0 = Negative0 + 1
            else:
                pass
            res1 = test_rate(f_maze)
            if  res1 == 1:
                Postive1 = Postive1 + 1
            elif res1 == -1:
                Negative1 = Negative1 + 1
            else:
                pass
        rate0 = Postive0/(Postive0 + Negative0)
        rate1 = Postive1/(Postive1 + Negative1)
        print("success rate of traditional way when q = {} is : {}".format(q, rate1))
        print("success rate of improved way when q = {} is : {}".format(q, rate0))
    # print("Test traditional algorithm:")
    # for q in range(4,11):
    #     q = q/10
    #     Postive = 0
    #     Negative = 0
    #     for i in range(1000):
    #         res = test_rate(p,q)
    #         if  res == 1:
    #             Postive = Postive + 1
    #         elif res == -1:
    #             Negative = Negative + 1
    #         else:
    #             pass
    #     rate = Postive/(Postive + Negative)
    #     print("success rate when q = {} is : {}".format(q, rate))

if __name__ == "__main__":
    main(0.2)
    # for p in [0.1, 0.15, 0.2, 0.25, 0.3]:
    #     main(p)
import queue
import maze as mazepkg
import numpy

PATH=100

class Bd_BFS:

    def __init__(self, dim, p):
        self.node_visited=None
        self.node_visited = None
        self.dim = dim
        self.p = p
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
        if self.node_visited != None:
            print("Node visited is {}".format(self.node_visited))
            return self.node_visited

    def get_path_length(self):
        print("Path length is {}".format(self.path_length))
        return self.path_length
    def neighbour(self,node):
        '''
        return a list of tuple with (coorY,coorX)
        which was not filled(obstacle)
        and is the neighbour of the curent one
        :param node（coor_y,coor_x）:
        :param maze: 2d list
        :return: list of tuple
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

    def find_path(self):
        '''
        node=（coor_y,coor_x）
        :param maze:
        :return:a list contain element[node:tuple,start_path:dic,start_path:dic]
        '''
        sizeY = len(self.maze)
        sizeX = len(self.maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1
        visited_start=[]
        visited_end=[]
        start_path={}
        end_path={}
        start_node=(0,0)
        end_node=(max_coorY,max_coorX)
        q_start=queue.Queue()
        q_end=queue.Queue()
        visited_end.append(end_node)
        visited_start.append(start_node)
        q_start.put(start_node)
        q_end.put(end_node)

        while not q_start.empty() and not q_end.empty():#if either side is empty there is no path generated
            #start first check
            current_start=q_start.get()
            for each_node in self.neighbour(current_start):
                if each_node not in visited_start:
                    visited_start.append(each_node)
                    q_start.put(each_node)
                    start_path[each_node]=current_start
                    if each_node in visited_end:
                        # print(end_path)
                        self.node_visited=len(visited_start)+len(visited_end)
                        return [each_node,start_path,end_path]


            # end second check
            current_end=q_end.get()
            for each_node in self.neighbour(current_end):
                if each_node not in visited_end:
                    visited_end.append(each_node)
                    q_end.put(each_node)
                    end_path[each_node] = current_end
                    if each_node in visited_start:
                        # print(end_path)
                        self.node_visited=len(visited_start)+len(visited_end)
                        return [each_node,start_path,end_path]


        else:

            return None

    def trace_back(self):
        '''
        print the path when existed
        :param maze:
        :return:
        '''
        if self.find_path()==None:
            print("no path found")
            return False
        else:
            print("find path")
            node,start_path,end_path = self.find_path()
            sizeY = len(self.maze)
            sizeX = len(self.maze[0])
            max_coorY = sizeY - 1
            max_coorX = sizeX - 1
            current = node

            while current != (0, 0):
                self.maze[current[0]][current[1]] = PATH
                current = start_path[current]
            self.maze[0][0] = PATH
            current = node
            while current != (max_coorY, max_coorX):
                self.maze[current[0]][current[1]] = PATH
                current = end_path[current]
            self.maze[max_coorY][max_coorX]=PATH
            # print ("the center node is {}".format(node))
            return True




    def calculate_path (self):
        '''

        :param maze: a maze which is path found maze, which mean 0 represent empty 1 represent filled 100 represent path
        :return:  total path
        '''

        path_length=numpy.sum(self.maze==PATH)
        self.path_length=path_length
        # print("total path length is {}".format(path_length))
    def print_final_path(self):

        print(numpy.matrix(self.maze))




if __name__ == "__main__":
    a = Bd_BFS(dim=10, p=0.3)


    a.get_path_length()
    a.get_node_visited()
    a.print_final_path()




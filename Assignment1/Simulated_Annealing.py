from Assignment1 import A_Manhattan_Class as a_manhattam
import maze as mazepkg
import numpy
import copy
import random

EMPTY = 0
FILLED = 1

class findHardMaze:
    def __init__(self,dim,p):
        maze_object=mazepkg.Maze(dim=dim,p=p)
        self.maze=maze_object.maze
        self.dim=dim
        self.p=p


    def print_maze(self):
        print(numpy.matrix(self.maze))
    def check_node_expended_Aalgo(self, tempmaze):#do not change maze:
        manhattan = a_manhattam.A_Manhattan(dim=10, p=1)
        temp=copy.deepcopy(tempmaze)
        manhattan.maze = temp
        manhattan.runMaze()
        return manhattan.get_node_visited()
        # manhattan.print_final_path()
        # manhattan.get_path_length()
    def sim_annealing(self):

        if not self.solvable():
            print("initial map cannot be solved")
            self.print_maze()
            return
        else:
            initial=self.maze
            tempmaze = copy.deepcopy(self.maze)
            t=1
            statelist=[]
            while True:

                t=1/t
                tempmaze=self.valid_random_maze(tempmaze)

                if self.check_node_expended_Aalgo(tempmaze)>self.check_node_expended_Aalgo(self.maze):
                    self.maze=tempmaze
                    self.pop(statelist)
                    print("1 case")

                else:
                    print(self.possibility(tempmaze,self.maze,t))
                    if self.check_node_expended_Aalgo(tempmaze)<self.check_node_expended_Aalgo(self.maze) and random.random()<self.possibility(tempmaze,self.maze,t):
                        print("2 case")
                        self.maze = tempmaze
                        self.pop(statelist)
                    else:#unchange
                        print("3 case")
                        statelist.append(True)
                        # print(statelist)
                        if len(statelist)==200:
                            print("hardest maze found")
                            self.check_result()
                            break




    def pop(self,statelist):
        if len(statelist)>0:
            statelist.pop()



    def possibility(self,new,current,t):
        k=1
        p=numpy.exp(-k * (self.check_node_expended_Aalgo(current) - self.check_node_expended_Aalgo(new)) / t)
        return p

    def neigbor_maze(self,tempmaze):



        #add a random obstacle and remove one
        while True:# add first
            randnode = self.generate_random_node()
            # print(randnode)
            if  not self.node_isFilled(tempmaze,randnode):
                tempmaze[randnode[0]][randnode[1]]=FILLED
                break

        while True:# add first
            randnode = self.generate_random_node()
            if   self.node_isFilled(tempmaze,randnode):
                tempmaze[randnode[0]][randnode[1]]=EMPTY
                break
        return tempmaze


    def generate_random_node(self):
        randx = random.randint(0, self.dim - 1)
        randy = random.randint(0, self.dim - 1)
        return (randy,randx)

    def node_isFilled(self, tempmaze, node): #check tempmaze
        randy=node[0]
        randx=node[1]
        if tempmaze[randy][randx]==FILLED:
            return True
        else:
            return False

    def solvable(self):# do not change maze
        manhattan = a_manhattam.A_Manhattan(dim=10, p=1)
        temp = copy.deepcopy(self.maze)
        manhattan.maze = temp
        manhattan.runMaze()
        return  manhattan.solvable
    def check_solvable(self,maze):
        manhattan = a_manhattam.A_Manhattan(dim=10, p=1)
        temp = copy.deepcopy(maze)
        manhattan.maze = temp
        manhattan.runMaze()
        return manhattan.solvable

    def is_same(self,new,current):
        return  new==current

    def valid_random_maze(self,maze):
        while True:
            temp=copy.deepcopy(maze)
            tempmaze = self.neigbor_maze(temp)
            if self.check_solvable(tempmaze):
                return tempmaze
    def check_result(self):

        manhattan = a_manhattam.A_Manhattan(dim=10, p=1)
        temp = copy.deepcopy(self.maze)
        manhattan.maze = temp
        manhattan.print_original_maze()
        manhattan.runMaze()
        manhattan.get_node_visited()
        manhattan.print_final_path()



















if __name__ == "__main__":
    algo=findHardMaze(10,0.2)
    algo.sim_annealing()




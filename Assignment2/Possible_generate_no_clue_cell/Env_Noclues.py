from Env import map
import random
import numpy

SAFE = 0
NO_CLUE=999
MINE = 1


class map_possible_noclues(map):
    def __init__(self,dim,num,p):
        '''

        :param dim:
        :param num:
        :param p: possibility to generate no clue safe cell
        '''
        map.__init__(self,dim,num)
        self.p=p
        self.random_map = numpy.arange(self.dim * self.dim).reshape(self.dim, self.dim)
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if self.is_clue_existed():
                    self.random_map[i, j] = 1
                else :
                    self.random_map[i,j]=0



    def query(self, x, y):
        if x >= 0 and x <= self.dim-1 and y >= 0 and y <= self.dim-1:
            if self.map[x, y] == MINE:
                return -1
            clues = 0


            for cell in self.neighbors(x, y):
                if self.map[cell] == MINE:
                    clues = clues + 1
            if self.random_map[x,y]==1:
                return clues
            elif self.random_map[x,y]==0:
                print("query no clue return")
                return NO_CLUE


        else:
            print("the location is out of bound")

    def is_clue_existed(self):
        if random.random()<self.p:
            print("no clues")
            return False
        else:
            return True



if __name__ == "__main__":
    print("10x10 with 10 mines")
    mine_map = map_possible_noclues(10, 10,0.2)
    mine_map.print_map()
    for i in range(10):
        for j in range(10):
            mine_map.query(i,j)

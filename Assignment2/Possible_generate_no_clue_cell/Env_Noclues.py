from Assignment2.Env import map
import random

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



    def query(self, x, y):
        if x >= 0 and x <= self.dim-1 and y >= 0 and y <= self.dim-1:
            if self.map[x, y] == MINE:
                return -1
            clues = 0
            if not self.is_clue_existed():
                return NO_CLUE

            for cell in self.neighbors(x, y):
                if self.map[cell] == MINE:
                    clues = clues + 1
            return clues
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

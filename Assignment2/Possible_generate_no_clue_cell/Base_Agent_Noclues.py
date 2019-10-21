import numpy
import random
from Assignment2.Possible_generate_no_clue_cell import Env_Noclues

HIDDEN = -2
MINE = -1
NO_CLUE=999

class Base_Agent(object):

    def __init__(self, env: Env_Noclues.map):
        self.env = env
        self.dim = env.dim
        self.map = numpy.arange(self.dim * self.dim).reshape(self.dim, self.dim)
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                self.map[i, j] = HIDDEN

        self.mines = set()
        self.hidden = set()
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                self.hidden.add((i, j))
        self.safe = set()
        self.reveal = 0
        self.miss = 0
        self.picked = set()

    def run(self):
        while len(self.hidden) >0:
            self.pick()
        print("----------------------------------------------------")
        print("-1:mine" )
        print(">=0:safe cell represent clues")
        print("999: no clue we dig")

        print("final map we go is:")
        self.print_map()

    def pick(self):
        if not self.safe or self.safe.issubset(self.picked):
            for neigh in self.picked:
                self.update_knowledge(neigh, self.env.query(neigh[0], neigh[1]))
            if not self.hidden:
                return
            # self.print_map()
            cell = self.hidden.pop()
            # print(cell)
            # print(self.safe)
            self.picked.add(cell)
            clues = self.env.query(cell[0], cell[1])
            self.update_knowledge(cell, clues)
        else:
            cells = self.safe.difference(self.picked)
            cell = cells.pop()
            self.hidden.discard(cell)
            self.picked.add(cell)
            clues = self.env.query(cell[0], cell[1])
            self.update_knowledge(cell, clues)

    def update_knowledge(self, cell, clues):
        # print(cell, clues)
        # self.print_map()
        if clues == -1:
            self.map[cell] = MINE
            self.mines.add(cell) 
            self.picked.remove(cell)
            self.miss = self.miss + 1
            print("oops , we encounter bomb!!!!!________________________")
            # for neigh in self.safe_neighbors(cell):
            #     self.update_knowledge(neigh, self.env.query(neigh[0], neigh[1]))
        elif clues==NO_CLUE :
            print("this cell {} dig with no clue-------".format(cell))
            self.map[cell] = clues
            self.safe.add(cell)

        else:
            self.map[cell] = clues # update the cell with the num of indicated mines
            self.safe.add(cell)
            if clues == len(self.hidden_neighbors(cell)) + len(self.revealed_mines(cell)): 
                for i in self.hidden_neighbors(cell):
                    self.map[i] = MINE
                    self.reveal = self.reveal + 1
                    self.hidden.discard(i)
                    self.mines.add(i)
        #he total number of mines (the clue) minus the number of revealed mines is the number ofhidden neighbors, every hidden neighbor is a mine.
            # print(len(self.safe_neighbors(cell)))
            # print(len(self.hidden_neighbors(cell)))
            if len(self.env.neighbors(cell[0], cell[1])) - clues == len(self.safe_neighbors(cell)) + len(self.hidden_neighbors(cell)):
            #the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors isthe number of hidden neighbors, every hidden neighbor is safe
                for i in self.hidden_neighbors(cell):
                    self.safe.add(i)
                    self.hidden.discard(i)


            # for neigh in self.picked:
            #     self.update_knowledge(neigh, self.env.query(neigh[0], neigh[1]))
        
    def hidden_neighbors(self, cell):
        res = self.env.neighbors(cell[0], cell[1])
        delt = []
        for i in res:
            if self.map[i] != HIDDEN:
                delt.append(i)
        for i in delt:
            res.remove(i)
        return res

    def revealed_mines(self, cell):
        res = self.env.neighbors(cell[0], cell[1])
        delt = []
        for i in res:
            if self.map[i] != MINE:
                delt.append(i)
        for i in delt:
            res.remove(i)
        return res

    def safe_neighbors(self, cell):
        res = self.env.neighbors(cell[0], cell[1])
        # print(res)
        delt = []
        for i in res:
            # print(i)
            # print(self.map[i])
            if self.map[i] < 0: # safe cell is larger than 0
                delt.append(i)
        for i in delt:
            res.remove(i)
        return res

    def print_map(self):
        print(numpy.matrix(self.map))

    def show_knowledge(self):
        print("Safe cells:", self.safe)
        print("Marked mines:", self.mines)


def calculate_average(num):
    sum=0
    for i in range(num):
        mine_map = Env_Noclues.map_possible_noclues(10, 60,0.2)
        agent = Base_Agent(mine_map)
        agent.run()
        # agent.print_map()
        # agent.pick()
        # agent.pick()
        # agent.print_map()
        agent.show_knowledge()
        score=agent.reveal / agent.env.mines
        sum+=score
        print("score: {}".format(agent.reveal / agent.env.mines))
    print("average {}".format(sum/num))
    return  sum/num

if __name__ == "__main__":
    # mine_map = Env.map(10, 40)
    # agent = Base_Agent(mine_map)
    # agent.run()
    # # agent.print_map()
    # # agent.pick()
    # # agent.pick()
    # # agent.print_map()
    # agent.show_knowledge()
    # print("score: {}".format(agent.reveal/agent.env.mines))
    calculate_average(20)




    
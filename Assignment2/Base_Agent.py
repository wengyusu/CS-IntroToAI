import numpy
import random
import Env

HIDDEN = -2
MINE = -1

class Base_Agent(object):

    def __init__(self, env: Env.map):
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
        self.picked = set()

    

    def pick(self):
        if not self.safe or self.safe.issubset(self.picked):
            cell = self.hidden.pop()
            self.picked.add(cell)
            clues = self.env.query(cell[0], cell[1])
            self.update_knowledge(cell, clues)
        else:
            cells = self.safe.difference(self.picked)
            cell = cells.pop()
            self.picked.add(cell)
            clues = self.env.query(cell[0], cell[1])
            self.update_knowledge(cell, clues)

    def update_knowledge(self, cell, clues):
        if clues == -1:
            self.map[cell] == MINE
            self.mines.add(cell)
            self.picked.remove(cell)
        else:
            self.map[cell] = clues # update the cell with the num of indicated mines
            self.safe.add(cell)
            if clues == len(self.hidden_neighbors(cell)) + len(self.revealed_mines(cell)): 
                for i in self.hidden_neighbors(cell):
                    self.map[i] == MINE
                    self.hidden.remove(i)
                    self.mines.add(i)
        #he total number of mines (the clue) minus the number of revealed mines is the number ofhidden neighbors, every hidden neighbor is a mine.
            # print(len(self.safe_neighbors(cell)))
            # print(len(self.hidden_neighbors(cell)))
            if 8 - clues == len(self.safe_neighbors(cell)) + len(self.hidden_neighbors(cell)):
            #the total number of safe neighbors (8 - clue) minus the number of revealed safe neighbors isthe number of hidden neighbors, every hidden neighbor is safe
                for i in self.hidden_neighbors(cell):
                    self.safe.add(i)
                    self.hidden.discard(i)
        
    def hidden_neighbors(self, cell):
        res = self.env.neighbors(cell[0], cell[1])
        for i in res:
            if self.map[i] != HIDDEN:
                res.remove(i)
        return res

    def revealed_mines(self, cell):
        res = self.env.neighbors(cell[0], cell[1])
        for i in res:
            if self.map[i] != MINE:
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

if __name__ == "__main__":
    mine_map = Env.map(10, 10)
    agent = Base_Agent(mine_map)
    # agent.print_map()
    agent.pick()
    agent.pick()
    agent.print_map()
    agent.show_knowledge()



    
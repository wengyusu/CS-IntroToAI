import numpy
import random

SAFE = 0
MINE = 1

class map(object):
    def __init__(self, dim, num):
        self.dim = dim
        self.map = numpy.zeros((dim, dim))
        self.mines = num

        n = num
        while n > 0:
            x = random.randint(0, dim-1)
            y = random.randint(0, dim-1)
            while self.map[x, y] == MINE:
                x = random.randint(0, dim-1)
                y = random.randint(0, dim-1)
            self.map[x, y] = MINE
            n = n -1

    def print_map(self):
        print(numpy.matrix(self.map))

    def neighbors(self, x, y):
        res= []
        if x > 0:
            res.append((x-1, y))
        if y > 0:
            res.append((x, y-1))
        if x < self.dim-1:
            res.append((x+1, y))
        if y < self.dim-1:
            res.append((x, y+1))
        if x > 0 and y > 0:
            res.append((x-1, y-1))
        if x > 0 and y < self.dim-1:
            res.append((x-1, y+1))
        if x < self.dim-1 and y > 0:
            res.append((x+1, y-1))
        if x < self.dim-1 and y < self.dim-1:
            res.append((x+1, y+1)) 
        return res

    def query(self, x, y):
        if x >= 0 and x <= self.dim-1 and y >= 0 and y <= self.dim-1:
            if self.map[x, y] == MINE:
                return -1
            clues = 0
            for cell in self.neighbors(x, y):
                if self.map[cell] == MINE:
                    clues = clues + 1
            return clues
        else:
            print("the location is out of bound")

if __name__ == "__main__":
    print("10x10 with 10 mines")
    mine_map = map(10, 10)
    mine_map.print_map()
    mine_map.query(1,1)


    

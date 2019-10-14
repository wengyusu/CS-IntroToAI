import numpy
import random

SAFE = 0
MINE = 1

class map(object):
    def __init__(self, dim, num):

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
        if x < dim-1:
            res.append((x+1, y))
        if y < dim-1:
            res.append((x, y+1))
        if x > 0 and y > 0:
            res.append((x-1, y-1))
        if x > 0 and y < dim-1:
            res.append((x-1, y+1))
        if x < dim-1 and y > 0:
            res.append((x+1, y-1))
        if x < dim-1 and y < dim-1:
            res.append((x+1, y+1)) 
        return res

if __name__ == "__main__":
    print("10x10 with 10 mines")
    mine_map = map(10, 10)
    mine_map.print_map()


    

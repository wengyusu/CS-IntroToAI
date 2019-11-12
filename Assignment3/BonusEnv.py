import Env
import random

FLAT = 1
HILLY = 2
FORESTED = 3
CAVES = 4

class BonusEnv(Env.Map):

    def __init__(self, dim):
        super(BonusEnv, self).__init__(dim)
        self.NotType = None
        self.getNotType()

    def getNotType(self):
        candidates = [FLAT, HILLY, FORESTED, CAVES]
        candidates.remove(self.map[self.target])
        self.NotType = random.choice(candidates)

    def neighbors(self, x, y): # given x,y,dim,return the list of its neighbors
        result = []
        if x < self.dim-1:
            result.append((x+1, y))

        if y < self.dim-1:
            result.append((x, y+1))

        if x > 0:
            result.append((x-1, y))

        if y > 0:
            result.append((x, y-1))
        
        return result

    def updateTarget(self):
        self.target = random.choice(self.neighbors(self.target[0], self.target[1]))
        self.getNotType()

    def query(self, cell):
        res = super(BonusEnv, self).query(cell)
        self.updateTarget()
        return res




import Agent
import numpy as np
from BonusEnv import BonusEnv

class BonusAgent(Agent.Agent):

    def __init__(self, MapObeject: BonusEnv):
        super(BonusAgent, self).__init__(MapObeject)
        self.sum = self.sumOfNotType(self.mapObject.getTerrainType(self.mapObject.target))

    def sumOfNotType(self, terrainType):
        res = 0
        total = 0
        for i in range(self.mapObject.dim):
                for j in range(self.mapObject.dim):
                    total = total + self.belief[i, j]
                    if self.mapObject.getTerrainType((i, j)) != terrainType:
                        res = res + self.belief[i, j]
        # self.sum = res
        return res / total

    def updateBelief(self, pickedCell, result):
        pickedCell_NotFound_IsIn = self.mapObject.getTerrainType(pickedCell)
        if result == True:
            print("Do not need to update. You get the target")
            print("target is {}".format(pickedCell))
            return
        else:
            # print(self.belief)
            # total = 0 
            for i in range(self.mapObject.dim):
                for j in range(self.mapObject.dim):
                    updateCell = (i, j)
                    updateCell_NotFound_IsIn = self.mapObject.getTerrainType(updateCell)
                    if updateCell_NotFound_IsIn == self.mapObject.NotType:
                        self.belief[updateCell] = 0
                    else:
                        if updateCell!=pickedCell:
                            self.belief[updateCell] =  (1.0 * self.belief[updateCell]) / (1.0 - (self.belief[pickedCell] * (1.0 - self.negativeRate[pickedCell_NotFound_IsIn])))

                        else:
                            self.belief[updateCell] =  (self.negativeRate[updateCell_NotFound_IsIn] * self.belief[updateCell]) / (1.0 - (self.belief[updateCell] * (1.0 - self.negativeRate[updateCell_NotFound_IsIn])))
                    belief = np.zeros((self.mapObject.dim, self.mapObject.dim))

        total = 0
        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                for neighbor in self.mapObject.neighbors(i, j):
                    belief[i, j] = belief[i, j] + (self.belief[neighbor]/len(self.mapObject.neighbors(neighbor[0], neighbor[1])))
                total = total + belief[i, j]

        self.belief = belief
        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                self.belief[i, j] = self.belief[i, j]/ total

def testTwoRule():
    print("runing rule 1....")
    countTimes1=0
    for i in range(500):
        map = BonusEnv(50)
        agent = BonusAgent(map)
        agent.run_rule1()
        countTimes1+=agent.countTimes

    countTimes2 = 0
    for i in range(500):
        map = BonusEnv(50)
        agent = BonusAgent(map)
        agent.run_rule2()
        countTimes2+=agent.countTimes
    print("runing rule 1....")
    print("average search time is ", countTimes1 / 500)
    print("runing rule 2....")
    print("average search time is ", countTimes2 / 500)

if __name__ == "__main__":
    # map=BonusEnv(20)
    # agent=BonusAgent(map)
    # agent.run_rule2()

    testTwoRule()
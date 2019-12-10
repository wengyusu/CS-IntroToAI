import Agent
import numpy as np
from BonusEnv import BonusEnv
import random

class BonusAgent(Agent.Agent):

    def __init__(self, MapObeject: BonusEnv):
        super(BonusAgent, self).__init__(MapObeject)
        self.moves = 0
        self.oldPickedCell = None
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

    def run_rule1(self):
        print("based on rule 1")
        flag = True
        while flag:
            pickedCell = self.randomPickHighPossibilityContainingCell()
            if self.oldPickedCell:
                self.moves = self.getDistance(pickedCell, self.oldPickedCell) + self.moves
            self.countTimes += 1
            self.oldPickedCell = pickedCell
            if self.responseToPicked(pickedCell) == True:
                flag = False
                print("total times cost is {}".format(self.countTimes))
                print("total moves cost is {}".format(self.moves))
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell,False)

    def run_rule2(self):
        print("based on rule 2")
        flag = True
        while flag:
            pickedCell = self.randomPickHighPossibilityFindingCell()
            if self.oldPickedCell:
                self.moves = self.getDistance(pickedCell, self.oldPickedCell) + self.moves
            self.countTimes += 1
            self.oldPickedCell = pickedCell
            if self.responseToPicked(pickedCell) == True:
                flag = False
                print("total times cost is {}".format(self.countTimes))
                print("total moves cost is {}".format(self.moves))
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell, False)

    def getDistance(self, cell0, cell1):
        return abs(cell0[0]-cell1[0]) + abs(cell0[1]-cell1[1])

class Q4BonusAgent(BonusAgent):
    def __init__(self, MapObeject: BonusEnv):
        super(BonusAgent, self).__init__(MapObeject)
        self.oldPickedCell = None
        self.moves = 0
        self.weightBelief = np.zeros((self.mapObject.dim, self.mapObject.dim))

    def updateWeighBelief(self, pickedCell):
        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                self.weightBelief[i, j] = self.belief[i, j]/(self.getDistance(pickedCell, (i, j)) + 1)

    def updateBelief(self, pickedCell, result):
        self.updateWeighBelief(pickedCell)
        return super(BonusAgent, self).updateBelief(pickedCell, result)
        
    def randomPickHighPossibilityContainingCell(self):#rule1
        result = np.where(self.weightBelief == np.amax(self.weightBelief))
        listOfCoordinates = list(zip(result[0], result[1]))

        maxIndex = random.sample(listOfCoordinates, 1)[0]
        # print(type(minIndex))
        return maxIndex  ##tuple

    def randomPickHighPossibilityFindingCell(self):#rule2
        findPossibility=np.zeros((self.mapObject.dim,self.mapObject.dim))
        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                updateCell=(i,j)
                terrainType = self.mapObject.getTerrainType(updateCell)

                found_targetIn=1-self.negativeRate[terrainType]

                findPossibility[updateCell]=self.weightBelief[updateCell]*found_targetIn
        result = np.where(findPossibility == np.amax(findPossibility))
        listOfCoordinates = list(zip(result[0], result[1]))

        # print("based on rule 2 the list have high possibility is ", listOfCoordinates)
        # print(self.mapObject.map)
        # print(findPossibility)
        maxIndex = random.sample(listOfCoordinates, 1)[0]
        return maxIndex  ##tuple


def testTwoRule():
    print("runing rule 1....")
    countTimes1=0
    moves1=0
    for i in range(20):
        map = BonusEnv(50)
        agent = BonusAgent(map)
        agent.run_rule1()
        countTimes1+=agent.countTimes
        moves1+=agent.moves

    countTimes2 = 0
    moves2=0
    for i in range(20):
        map = BonusEnv(50)
        agent = BonusAgent(map)
        agent.run_rule2()
        countTimes2+=agent.countTimes
        moves2+=agent.moves
    print("runing rule 1....")
    print("average search time is ", countTimes1 / 20)
    print("average move time is ", moves1 / 20)
    print("runing rule 2....")
    print("average search time is ", countTimes2 / 20)
    print("average move time is ", moves2 / 20)

def Q4testTwoRule():
    print("runing Q4 with rule 1....")
    countTimes1=0
    moves1=0
    for i in range(10):
        map = BonusEnv(50)
        agent = Q4BonusAgent(map)
        agent.run_rule1()
        countTimes1+=agent.countTimes
        moves1+=agent.moves

    countTimes2 = 0
    moves2=0
    for i in range(10):
        map = BonusEnv(50)
        agent = Q4BonusAgent(map)
        agent.run_rule2()
        countTimes2+=agent.countTimes
        moves2+=agent.moves
    print("runing Q4 with rule 1....")
    print("average search time is ", countTimes1 / 10)
    print("average move time is ", moves1 / 10)
    print("runing rule 2....")
    print("average search time is ", countTimes2 / 10)
    print("average move time is ", moves2 / 10)

if __name__ == "__main__":
    # map=BonusEnv(20)
    # agent=BonusAgent(map)
    # agent.run_rule2()

    # testTwoRule()
    Q4testTwoRule()
    # map = BonusEnv(50)
    # agent = Q4BonusAgent(map)
    # agent.run_rule1()
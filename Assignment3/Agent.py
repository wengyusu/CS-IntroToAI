import numpy as np
import random
from Env import Map
import math

FLAT = 1
HILLY = 2
FORESTED = 3
CAVES = 4


class Agent:
    def __init__(self, MapObeject: Map):
        self.negativeRate = {1: 0.1, 2: 0.3, 3: 0.7, 4: 0.9}
        self.countTimes = 0
        self.mapObject = MapObeject
        print ("our target to dig is ",self.mapObject.target)
        self.belief = np.zeros((self.mapObject.dim, self.mapObject.dim))  # possibility of "target in"specific cell
        self.initBelief()



    def run_rule1(self):
        print("based on rule 1")
        flag = True
        while flag:

            pickedCell = self.randomPickHighPossibilityContainingCell()
            self.countTimes += 1
            if self.responseToPicked(pickedCell) == True:
                flag = False
                print("total times cost is {}".format(self.countTimes))
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell,False)

    def run_rule2(self):
        print("based on rule 2")
        flag = True
        while flag:

            pickedCell = self.randomPickHighPossibilityFindingCell()
            self.countTimes += 1
            if self.responseToPicked(pickedCell) == True:
                flag = False
                print("total times cost is {}".format(self.countTimes))
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell, False)



    def initBelief(self):
        totalCells = math.pow(self.mapObject.dim, 2)
        p = 1 / totalCells
        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                self.belief[i, j] = p


    def randomPickHighPossibilityContainingCell(self):#rule1
        result = np.where(self.belief == np.amax(self.belief))
        listOfCoordinates = list(zip(result[0], result[1]))

        # print("based on rule 1 the list have high possibility is ",listOfCoordinates)
        # print(self.mapObject.map)
        # print(self.belief)
        # for cord in listOfCordinates:
        #         #     print(cord)
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

                findPossibility[updateCell]=self.belief[updateCell]*found_targetIn
        result = np.where(findPossibility == np.amax(findPossibility))
        listOfCoordinates = list(zip(result[0], result[1]))

        # print("based on rule 2 the list have high possibility is ", listOfCoordinates)
        # print(self.mapObject.map)
        # print(findPossibility)
        maxIndex = random.sample(listOfCoordinates, 1)[0]
        return maxIndex  ##tuple




    def responseToPicked(self, cell):
        # print("we pick ",cell)
        return self.mapObject.query(cell)

    def targetNotFoundInCell_TargetIsInCell(self, terrainType):


        # dict={1:0.1,2:0.3,3:0.7,4:0.9}
        return self.negativeRate[terrainType]


    def updateBelief(self, pickedCell, result):
        pickedCell_NotFound_IsIn = self.mapObject.getTerrainType(pickedCell)
        temp=self.belief[pickedCell]
        if result == True:
            print("Do not need to update. You get the target")
            print("target is {}".format(pickedCell))
            return
        else:
            for i in range(self.mapObject.dim):
                for j in range(self.mapObject.dim):
                    updateCell = (i, j)
                    updateCell_NotFound_IsIn = self.mapObject.getTerrainType(updateCell)
                    if updateCell!=pickedCell:
                        self.belief[updateCell] = (1.0 * self.belief[updateCell]) / (1.0 - (temp * (1.0 - self.negativeRate[pickedCell_NotFound_IsIn])))


                    else:
                        self.belief[updateCell] = (self.negativeRate[updateCell_NotFound_IsIn] * self.belief[updateCell]) / (1.0 - (self.belief[updateCell] * (1.0 - self.negativeRate[updateCell_NotFound_IsIn])))

def testTwoRule():
    print("runing rule 1....")
    countTimes1=0
    for i in range(500):
        map = Map(50)
        agent = Agent(map)
        agent.run_rule1()
        countTimes1+=agent.countTimes

    countTimes2 = 0
    for i in range(500):
        map = Map(50)
        agent = Agent(map)
        agent.run_rule2()
        countTimes2+=agent.countTimes
    print("runing rule 1....")
    print("average search time is ", countTimes1 / 500)
    print("runing rule 2....")
    print("average search time is ", countTimes2 / 500)


def testOfNp():
    arr=np.zeros((10,10))
    for i in range (10):
        for j in range(10):
            arr[i,j]=random.random()
    result = np.where(arr == np.amax(arr))
    listOfCoordinates = list(zip(result[0], result[1]))
    print(listOfCoordinates)
    print(arr)










if __name__ == "__main__":
    # map=Map(50)
    # agent=Agent(map)
    # agent.run_rule2()

    testTwoRule()

    # testOfNp()



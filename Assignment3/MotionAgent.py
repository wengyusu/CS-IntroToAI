from Agent import Agent
from Env import Map
import  numpy as np
import random
class MotionAgent(Agent):
    '''
    we calculate total  motion  to evaluate the efficiency of the algorithm
    motion= search time + move_distance/10
    once we update belief of all cell based on possibility of finding or containing cell we will add corresponding weight and provide an optimal one to dig
    '''
    def __init__(self,Map):
        Agent.__init__(self,Map)
        self.currentCell=()
        self.totalDistance=0
        self.totalMotion=0


    def run_rule1_motion(self):
        print("based on rule 1")
        flag = True
        while flag:

            pickedCell = self.randomPickHighPossibilityContainingCell()
            # print("picked cell is ", pickedCell)
            self.totalDistance+=self.calculateStepDistance(pickedCell)
            self.countTimes += 1
            self.currentCell=pickedCell
            if self.responseToPicked(pickedCell) == True:
                flag = False
                print("total times cost is {}".format(self.countTimes))
                print("total distance is " ,self.totalDistance)
                self.totalMotion=self.countTimes+self.totalDistance
                print("totalMotion is ", self.totalMotion)
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell, False)
    def run_rule1_motionWithDistanceWeight(self):
        print("based on rule 1")
        flag = True
        while flag:

            pickedCell = self.randomPickHighPossibilityContainingCell_Motion()
            # print("picked cell is ", pickedCell)
            self.totalDistance+=self.calculateStepDistance(pickedCell)
            self.countTimes += 1
            self.currentCell=pickedCell
            if self.responseToPicked(pickedCell) == True:
                flag = False
                print("total times cost is {}".format(self.countTimes))
                print("total distance is " ,self.totalDistance)
                self.totalMotion=self.countTimes+self.totalDistance
                print("totalMotion is ", self.totalMotion)
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell, False)

    def run_rule2_motion(self):
        print("based on rule 2")
        flag = True
        while flag:

            pickedCell = self.randomPickHighPossibilityFindingCell()
            self.totalDistance += self.calculateStepDistance(pickedCell)
            self.countTimes += 1
            self.currentCell = pickedCell
            if self.responseToPicked(pickedCell) == True:
                flag = False

                print("total times cost is {}".format(self.countTimes))
                print("total distance is ", self.totalDistance)
                self.totalMotion = self.countTimes + self.totalDistance
                print("totalMotion is ", self.totalMotion)
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell, False)
    def run_rule2_motionWithDistanceWeight(self):
        print("based on rule 2")
        flag = True
        while flag:

            pickedCell = self.randomPickHighPossibilityFindingCell_Motion()
            self.totalDistance += self.calculateStepDistance(pickedCell)
            self.countTimes += 1
            self.currentCell = pickedCell
            if self.responseToPicked(pickedCell) == True:
                flag = False

                print("total times cost is {}".format(self.countTimes))
                print("total distance is ", self.totalDistance)
                self.totalMotion = self.countTimes + self.totalDistance
                print("totalMotion is ", self.totalMotion)
                print("terminate the iteration because we find the target {}".format(pickedCell))

            else:
                self.updateBelief(pickedCell, False)

    def randomPickHighPossibilityContainingCell_Motion(self):#rule1

        distanceWeightedPossibility = np.zeros((self.mapObject.dim, self.mapObject.dim))
        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                updateCell = (i, j)

                distance = self.calculateDistance(updateCell)
                weight = distance // 10 + 1
                distanceWeightedPossibility[updateCell] = 1 - pow((1 - self.belief[updateCell]), 1 / weight)



        result = np.where(distanceWeightedPossibility == np.amax(distanceWeightedPossibility))
        listOfCoordinates = list(zip(result[0], result[1]))

        # print("based on rule 1 the list have high possibility is ",listOfCoordinates)
        # print(self.mapObject.map)
        # print(self.belief)
        # for cord in listOfCordinates:
        #         #     print(cord)
        maxIndex = random.sample(listOfCoordinates, 1)[0]
        # print(type(minIndex))
        return maxIndex  ##tuple
    def randomPickHighPossibilityFindingCell_Motion(self):#rule2
        findPossibility=np.zeros((self.mapObject.dim,self.mapObject.dim))
        distanceWeightedPossibility = np.zeros((self.mapObject.dim, self.mapObject.dim))

        for i in range(self.mapObject.dim):
            for j in range(self.mapObject.dim):
                updateCell=(i,j)
                terrainType = self.mapObject.getTerrainType(updateCell)

                found_targetIn=1-self.negativeRate[terrainType]

                findPossibility[updateCell]=self.belief[updateCell]*found_targetIn
                distance=self.calculateDistance(updateCell)
                weight=distance//10+1
                distanceWeightedPossibility[updateCell]=1-pow((1-findPossibility[updateCell]),1/weight)
        result = np.where(distanceWeightedPossibility == np.amax(distanceWeightedPossibility))
        listOfCoordinates = list(zip(result[0], result[1]))

        print("based on rule 2 the list have high possibility is ", listOfCoordinates)
        print(self.mapObject.map)
        # print(findPossibility)
        maxIndex = random.sample(listOfCoordinates, 1)[0]
        return maxIndex  ##tuple

    def calculateStepDistance(self, cell):
        if not self.currentCell:
            self.currentCell=cell
            print("the first cell we choose without counting distance")
            return 0
        else:
            distance=abs(cell[0]-self.currentCell[0])+abs(cell[1]-self.currentCell[1])

        return distance

    def calculateDistance(self,cell):
        if not self.currentCell:
            return 0
        else:
            distance = abs(cell[0] - self.currentCell[0]) + abs(cell[1] - self.currentCell[1])
            return  distance

def testTwoRuleWithoutAddDistanceWeight():
    print("runing rule 1....")
    totalMotion1=0
    for i in range(10):
        map = Map(50)
        agent = MotionAgent(map)
        agent.run_rule1_motion()
        totalMotion1+=agent.totalMotion
    print("runing rule 2....")
    totalMotion2=0
    for i in range(10):
        map = Map(50)
        agent = MotionAgent(map)
        agent.run_rule2_motion()
        totalMotion2 += agent.totalMotion
    print("runing rule 1 with dim 50 and for 10 times ..")
    print("average search action is ", totalMotion1 / 10)
    print("runing rule 2 with dim 50 and for 10 times ..")
    print("average search action is ", totalMotion2 / 10)
def testTwoRuleWithAddDistanceWeight():
    print("runing rule 1....")
    totalMotion1=0
    for i in range(10):
        map = Map(50)
        agent = MotionAgent(map)
        agent.run_rule1_motionWithDistanceWeight()
        totalMotion1+=agent.totalMotion
    print("runing rule 2....")
    totalMotion2=0
    for i in range(10):
        map = Map(50)
        agent = MotionAgent(map)
        agent.run_rule2_motionWithDistanceWeight()
        totalMotion2 += agent.totalMotion
    print("runing rule 1 with dim 50 and for 10 times ..")
    print("average search action is ", totalMotion1 / 10)
    print("runing rule 2 with dim 50 and for 10 times ..")
    print("average search action is ", totalMotion2 / 10)




if __name__=="__main__":
    # map = Map(10)
    # agent = MotionAgent(map)
    # agent.run_rule2_motionWithDistanceWeight()
    # testTwoRuleWithoutAddDistanceWeight()
    testTwoRuleWithAddDistanceWeight()
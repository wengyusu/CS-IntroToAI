import numpy as np
import random

FLAT = 1
HILLY = 2
FORESTED = 3
CAVES = 4
class Map:



    def __init__(self,dim):

        self.dim=dim
        self.map=np.zeros((self.dim,self.dim))
        self.target =(random.randint(0,dim-1),random.randint(0,dim-1))
        for i in range(self.dim):
            for j in range(self.dim):
                currentCell=(i,j)
                self.map[currentCell]=self.generateType()








    def getTerrainType(self,cell):

        return self.map[cell]


    def generateType(self):
        p=random.random()
        if p>=0 and p<0.2:
            return  FLAT
        elif p>=0.2 and p<0.5:
            return HILLY
        elif p>=0.5 and p<0.8:
            return  FORESTED
        else:
            return  CAVES

    # def generateType(self):
    #     p = random.random()
    #     return FLAT


if __name__=="__main__":
    map=Map(4)
    # print(map.getTerrainType((2,2)))

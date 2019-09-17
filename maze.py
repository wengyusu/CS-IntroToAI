import numpy
import random

EMPTY = 0
FILLED = 1

dim = 10

p = 0.3

def probability(p):
    """ given an event of probability p, return whether the event comes true"""
    return (random.random()<p)

# for i in range(dim):
#     print("\n")
#     for j in range(dim):
#         print("{} ,".format(maze[i,j]))
# print(numpy.matrix(maze))

def sampleMAze():

    maze = numpy.zeros((dim, dim))

    for i in range(dim):
        for j in range(dim):
            if probability(p):
                maze[i, j] = 1
    maze[0, 0] = 0
    maze[1, 1] = 0
    return maze

maze=sampleMAze()
print(numpy.matrix(maze))

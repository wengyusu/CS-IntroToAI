import numpy
import random

EMPTY = 0
FILLED = 1

class Maze:
    def __init__(self, dim, p):
        self.dim = dim
        self.p = p
        self.maze = None
        self.generate_maze()

    def probability(self, p):
        """ given an event of probability p, return whether the event comes true"""
        return (random.random()<p)

    def generate_maze(self):
        self.maze = numpy.zeros((self.dim, self.dim))

        for i in range(self.dim):
            for j in range(self.dim):
                if self.probability(self.p):
                    self.maze[i, j] = FILLED
        self.maze[0,0] = EMPTY
        self.maze[self.dim-1, self.dim-1] = EMPTY

    def print_maze(self):
        if self.maze is not None:
            print(numpy.matrix(self.maze))
        else:
            print("You must generate the maze first")

if __name__ == "__main__":
    maze = Maze(11, 0.5)
    maze.print_maze()
    # help(maze)

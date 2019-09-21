from maze import Maze
import A_Euclidean_Distance
import A_Manhattan_Distance
import Bi_Directional_Breadth_First_Search
import numpy


def question4_forEuclidean(dim,p):
    for i in numpy.arange (0,p,0.01):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if A_Euclidean_Distance.trace_back(maze):
            print("p is {}".format(i))
            A_Euclidean_Distance.calculate_path (maze)
def question4_forManhattan(dim,p):
    for i in numpy.arange (0,p,0.01):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if A_Manhattan_Distance.trace_back(maze):
            print("p is {}".format(i))
            A_Manhattan_Distance.calculate_path (maze)
def question4_forBiDirection(dim,p):
    for i in numpy.arange (0,p,0.01):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if Bi_Directional_Breadth_First_Search.trace_back(maze):
            print("p is {}".format(i))
            Bi_Directional_Breadth_First_Search.calculate_path (maze)
            print("_________")




if __name__ == "__main__":
    # maze_object = maze.Maze(dim=10, p=0)
    # maze=maze_object.maze
    # # maze=maze.generate_maze()
    # #distanceE=generate_EuclideanDistance(maze)
    # print(numpy.matrix(maze))
    # # print(numpy.matrix(distanceE))
    # A_Euclidean_Distance.trace_back(maze)
    #  question4_forEuclidean(512,0.2)
    # question4_forManhattan(512,0.2)
    # question4_forBiDirection(100, 0.2)



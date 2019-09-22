from maze import Maze
import A_Euclidean_Distance
import A_Manhattan_Distance
import Bi_Directional_Breadth_First_Search
import numpy
import UniformSearch
import time
import copy


def question4_forEuclidean(dim,p,step=0.01):
    '''

    :param dim:
    :param p:
    :return: p from 0 to 0.2 calculate total path
    '''
    for i in numpy.arange (0,p,step):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if A_Euclidean_Distance.trace_back(maze):
            print("p is {}".format(i))
            A_Euclidean_Distance.calculate_path (maze)
def question4_forManhattan(dim,p,step=0.01):
    '''

    :param dim:
    :param p:
    :return: p from 0 to 0.2 calculate total path
    '''
    for i in numpy.arange (0,p,step):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if A_Manhattan_Distance.trace_back(maze):
            print("p is {}".format(i))
            A_Manhattan_Distance.calculate_path (maze)
def question4_forBiDirection(dim,p,step=0.01):
    '''

    :param dim:
    :param p:
    :return: p from 0 to 0.2 calculate total path
    '''
    for i in numpy.arange (0,p,step):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if Bi_Directional_Breadth_First_Search.trace_back(maze):
            print("p is {}".format(i))
            Bi_Directional_Breadth_First_Search.calculate_path (maze)
            print("_________")

def question5_UniformSearch(dim, p,step=0.01):
    '''

    :param dim:
    :param p:
    :return: p from 0 to 0.2 calculate total path
    '''
    for i in numpy.arange(0, p, step):
        maze_object = Maze(dim=dim, p=i)
        maze = maze_object.maze
        if UniformSearch.trace_back(maze):
            print("p is {}".format(i))
            UniformSearch.calculate_path(maze)
def compare_time(dim,p,step):
    '''
    compare 3 different algorithm time cost
    :return: dispaly on screen
    '''

    start_time = time.time()
    question5_UniformSearch(dim, p, step)
    print("total time cost using Uniform search is {}".format(time.time() - start_time))


    start_time = time.time()
    question4_forManhattan(dim, p,step)
    print("total time cost using Manhattan search is {}".format(time.time() - start_time))
    start_time = time.time()
    question4_forEuclidean(dim, p,step)
    print("total time cost using Euclidean search is {}".format(time.time() - start_time))


def question8(dim,p):
    maze_object = Maze(dim=dim, p=p)
    maze = maze_object.maze
    same_maze=copy.deepcopy(maze)
    same_maze2=copy.deepcopy(maze)
    A_Manhattan_Distance.print_path(maze)
    A_Euclidean_Distance.print_path(same_maze)
    Bi_Directional_Breadth_First_Search.print_path(same_maze2)


if __name__ == "__main__":
    # question4_forEuclidean(512,0.2)
    # question4_forManhattan(512,0.2)
    #question4_forBiDirection(100, 0.2)
    # compare_time(1024,0.2,0.02)
    question8(256,0.2)




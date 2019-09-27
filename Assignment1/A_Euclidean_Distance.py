import maze
import numpy
import math
import heapq

PATH=100

def generate_EuclideanDistance(maze):
    '''
    set heuristic "h"
    suppose coorX is len(maze)
    suppose coorY is len(maze[0])
    maze[y][x]
    '''
    sizeY=len(maze)
    sizeX=len(maze[0])
    max_coorY=sizeY-1
    max_coorX=sizeX-1
    distance_Euclidean=[[0] * sizeX for i in range(sizeY)]
    for x in range(sizeX):
        for y in range(sizeY):
            distance_Euclidean[x][y]=math.sqrt(((max_coorX-x)**2+(max_coorY-y)**2))
    distance_Euclidean[0][0]=0
    return distance_Euclidean





def neighbour(node,maze):
    '''
    return a list of tuple with (coorY,coorX)
    which was not filled(obstacle)
    and is the neighbour of the curent one
    :param node:
    :param maze:
    :return:
    '''
    neighbour_node=[]
    coor_x=node[1]
    coor_y=node[0]
    sizeY=len(maze)
    sizeX=len(maze[0])
    max_coorY=sizeY-1
    max_coorX=sizeX-1

    if coor_x>0:
        x_minus_one = coor_x - 1
        letf_one = (coor_y, x_minus_one)
        if (maze[coor_y][x_minus_one]) == 0:
            neighbour_node.append(letf_one)

    if coor_x<max_coorX:
        x_plus_one = coor_x + 1
        right_one = (coor_y, x_plus_one)
        if (maze[coor_y][x_plus_one]) == 0:
            neighbour_node.append(right_one)

    if coor_y > 0:
        y_minus_one = coor_y - 1
        below_one = (y_minus_one, coor_x)
        if (maze[y_minus_one][coor_x]) == 0:
            neighbour_node.append(below_one)

    if coor_y < max_coorY:
        y_plus_one = coor_y + 1
        above_one = (y_plus_one, coor_x)
        if (maze[y_plus_one][coor_x]) == 0:
            neighbour_node.append(above_one)
    return neighbour_node


def generate_path(maze):
    '''
    using 2d list track the previous node
    :param maze:
    :return:
    '''
    sizeY = len(maze)
    sizeX = len(maze[0])
    max_coorY = sizeY - 1
    max_coorX = sizeX - 1
    distanceE = generate_EuclideanDistance(maze)
    pq=[]
    path={}
    visited=[[False]*sizeX for i in range(sizeY)]
    costed= [[0] * sizeX for i in range(sizeY)]
    heapq.heappush(pq,(0,(0,0)))
    visited[0][0]=True
    while len(pq)!=0:
        node=heapq.heappop(pq)[1]
        if node==(max_coorX,max_coorY):
            print("Node visited is {}".format(numpy.sum(visited)))
            print("find path:")
            break
        for (coor_y,coor_x) in neighbour(node,maze):
            if not visited[coor_y][coor_x]:
                costed[coor_y][coor_x]=costed[node[0]][node[1]]+1
                visited[coor_y][coor_x]=True
                heapq.heappush(pq,(costed[coor_y][coor_x]+distanceE[coor_y][coor_x],(coor_y,coor_x)))
                path[(coor_y,coor_x)]=(node[0],node[1])
    return path
def trace_back(maze):
    '''
    print the path when existed
    :param maze:
    :return:
    '''
    path=generate_path(maze)
    sizeY = len(maze)
    sizeX = len(maze[0])
    max_coorY = sizeY - 1
    max_coorX = sizeX - 1
    current=(max_coorY,max_coorX)
    if current not in path:
        print("no path found")
        return False
    while current!=(0,0):
        maze[current[0]][current[1]]=PATH
        current=path[current]
    maze[0][0]=PATH


    return True

def calculate_path (maze):
    '''
    :param maze: a maze which is path found maze, which mean 0 represent empty 1 represent filled 100 represent path
    :return:  total path
    '''
    path_length=numpy.sum(maze==PATH)
    print("total path length is {}".format(path_length))



    
    

def print_path(maze):
    '''
    :param maze:  a maze generated randomly
    :return: print original maze and path-found maze(100 represent "Path")
    '''
    print(numpy.matrix(maze))
    trace_back(maze)
    print(numpy.matrix(maze))
    calculate_path(maze)







if __name__=="__main__":
    maze_object = maze.Maze(dim=10, p=0.2)
    maze=maze_object.maze # generate a maze
    print_path(maze) #print original maze and path-found maze(100 represent "Path")
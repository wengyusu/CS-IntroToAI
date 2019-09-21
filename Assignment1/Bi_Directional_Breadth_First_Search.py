import queue
import maze
import numpy

PATH=100



def neighbour(node, maze):
    '''
    return a list of tuple with (coorY,coorX)
    which was not filled(obstacle)
    and is the neighbour of the curent one
    :param node（coor_y,coor_x）:
    :param maze: 2d list
    :return: list of tuple
    '''
    neighbour_node = []
    coor_x = node[1]
    coor_y = node[0]
    sizeY = len(maze)
    sizeX = len(maze[0])
    max_coorY = sizeY - 1
    max_coorX = sizeX - 1

    if coor_x > 0:
        x_minus_one = coor_x - 1
        letf_one = (coor_y, x_minus_one)
        if (maze[coor_y][x_minus_one]) == 0:
            neighbour_node.append(letf_one)

    if coor_x < max_coorX:
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

def find_path(maze):
    '''
    node=（coor_y,coor_x）
    :param maze:
    :return:a list contain element[node:tuple,start_path:dic,start_path:dic]
    '''
    sizeY = len(maze)
    sizeX = len(maze[0])
    max_coorY = sizeY - 1
    max_coorX = sizeX - 1
    visited_start=[]
    visited_end=[]
    start_path={}
    end_path={}
    start_node=(0,0)
    end_node=(max_coorY,max_coorX)
    q_start=queue.Queue()
    q_end=queue.Queue()
    visited_end.append(end_node)
    visited_start.append(start_node)
    q_start.put(start_node)
    q_end.put(end_node)

    while not q_start.empty() and not q_end.empty():#if either side is empty there is no path generated
        #start first check
        current_start=q_start.get()
        for each_node in neighbour(current_start,maze):
            if each_node not in visited_start:
                visited_start.append(each_node)
                q_start.put(each_node)
                start_path[each_node]=current_start
                if each_node in visited_end:
                    # print(end_path)
                    return [each_node,start_path,end_path]

        # end second check
        current_end=q_end.get()
        for each_node in neighbour(current_end,maze):
            if each_node not in visited_end:
                visited_end.append(each_node)
                q_end.put(each_node)
                end_path[each_node] = current_end
                if each_node in visited_start:
                    # print(end_path)
                    return [each_node,start_path,end_path]


    else:

        return None

def trace_back(maze):
    '''
    print the path when existed
    :param maze:
    :return:
    '''
    if find_path(maze)==None:
        print("no path found")
        return False
    else:
        node,start_path,end_path = find_path(maze)
        sizeY = len(maze)
        sizeX = len(maze[0])
        max_coorY = sizeY - 1
        max_coorX = sizeX - 1
        current = node

        while current != (0, 0):
            maze[current[0]][current[1]] = PATH
            current = start_path[current]
        maze[0][0] = PATH
        current = node
        while current != (max_coorY, max_coorX):
            maze[current[0]][current[1]] = PATH
            current = end_path[current]
        maze[max_coorY][max_coorX]=PATH
        print ("the center node is {}".format(node))
        return True




def calculate_path (maze):

    path_length=numpy.sum(maze==PATH)
    print("total path length is {}".format(path_length))
def print_path(maze):
    print(numpy.matrix(maze))
    trace_back(maze)
    print(numpy.matrix(maze))
    calculate_path(maze)



if __name__ == "__main__":
    maze_object = maze.Maze(dim=100, p=0.3)
    maze = maze_object.maze
    # # maze=maze.generate_maze()
    # # distanceE=generate_EuclideanDistance(maze)
    # print(numpy.matrix(maze))
    # # print(numpy.matrix(distanceE))
    # trace_back(maze)  # test
    print_path(maze)

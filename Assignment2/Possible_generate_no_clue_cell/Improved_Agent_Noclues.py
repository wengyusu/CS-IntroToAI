from Base_Agent_Noclues import Base_Agent
import numpy
import random
import Env_Noclues
import copy
import heapq
from itertools import combinations, permutations
HIDDEN = -2
MINE = -1
TEMP_SAFE=100
NO_CLUE=999

class Improved_Agent(Base_Agent):

    def __init__(self,env: Env_Noclues.map):
        Base_Agent.__init__(self,env)
        self.candidate_100safe=set()
        self.candidate_guess_heap=[]
        self.candidate_high_safe_list =[]
        self.candidate_cell=()

    def pick(self):
        if not self.safe or self.safe.issubset(self.picked):
            for neigh in self.picked:

                self.update_knowledge(neigh, self.env.query(neigh[0], neigh[1]))
                # print("first update map")
                # self.print_map()
            print("before new we update again")
            self.print_map()
            if not self.hidden:
                return
            if not self.safe.issubset(self.picked):
                print("double check update again")
                return
            self.loop_each_picked_element()
            # self.print_map()
            if self.candidate_100safe:
                cell = self.candidate_100safe.pop()
                self.hidden.discard(cell)
            elif self.candidate_cell:
                cell = self.candidate_cell
                self.hidden.discard(cell)
            # cell = self.hidden.pop()
            else:
                print("we pick randomly")
                cell=self.hidden.pop()

            print("The cell we finally pick is {}".format(cell))
            self.print_map()
            # print(self.safe)
            self.picked.add(cell)
            clues = self.env.query(cell[0], cell[1])
            self.update_knowledge(cell, clues)
            print("after dig we got:")
            self.print_map()
        else:
            cells = self.safe.difference(self.picked)
            print("the cell we haven't dig but safe is {}".format(cells))
            cell = cells.pop()
            self.hidden.discard(cell)
            self.picked.add(cell)
            clues = self.env.query(cell[0], cell[1])
            self.update_knowledge(cell, clues)
            print("after we dig one of the safe cell we got")
            self.print_map()
    def loop_each_picked_element(self):
        self.candidate_guess_heap = []
        if self.picked:


            for pick_element in self.picked:
                # print(" the pick element we loop is {}".format(pick_element))
                clue=self.env.query(pick_element[0],pick_element[1])#for each pick get the clue
                if clue==NO_CLUE:
                    print("skip because we think there is no clue so we cannot add this cell in potential heap")
                    continue
                hidden_neighbors=self.hidden_neighbors(pick_element)
                revealed_mines=self.revealed_mines(pick_element)
                safe_neighbors=self.safe_neighbors(pick_element)
                total_neighbors=len(hidden_neighbors)+len(revealed_mines)+len(safe_neighbors)#konw the location in the board
                # print("total_neighbors")
                # print(total_neighbors)
                # print(pick_element)
                if(len(hidden_neighbors)==0):#make sure exist hidden one to continue
                    continue
                hiddden_neighbor_mine=clue-len(revealed_mines)
                # print(hiddden_neighbor_mine)
                # print(len(hidden_neighbors))
                choice_boom_rate=hiddden_neighbor_mine/len(hidden_neighbors)
                if (hiddden_neighbor_mine==0 and len(hidden_neighbors)!=0):
                    self.candidate_100safe.union(hidden_neighbors)
                    return

                    # print(pick_element)
                    # self.print_map()
                else:

                    print("-----enter heap------------")
                    print(choice_boom_rate)
                    heapq.heappush(self.candidate_guess_heap,(-1*choice_boom_rate,pick_element))
                    print(pick_element)
            print("______enterassumption_____")
            self.make_assumption()



        print("------------------------")

    def make_assumption(self):
        # while True:
        self.candidate_cell = ()
        if(self.candidate_guess_heap):
            print("heap is {}".format(self.candidate_guess_heap))
            prior,cell=heapq.heappop(self.candidate_guess_heap)
            if -1*prior<=0.2:
                print("prior is two small to make assumption")
                self.candidate_cell=random.sample(self.hidden_neighbors(cell),1)[0]
                print("the random sample we get is {}".format(self.candidate_cell))
                return
            print("assumption cell is {}".format(cell))

            self.check_valid(cell)



    def check_valid(self,cell):#assume a bomb and check existing info
        self.candidate_high_safe_list=[]
        self.candidate_cell=()
        clue = self.env.query(cell[0], cell[1]) # for each pick get the clue

        hidden_neighbors = self.hidden_neighbors(cell)
        revealed_mines = self.revealed_mines(cell)
        safe_neighbors = self.safe_neighbors(cell)
        total_neighbors = len(hidden_neighbors) + len(revealed_mines) + len(
            safe_neighbors)  # konw the location in the board
        hidden_neighbor_mine_num = clue - len(revealed_mines)
        hidden_neighbors_num=len(hidden_neighbors)
        print("the cell is {}".format(cell))
        print("total hidden is {a} and hidden mine is {b}".format(a=hidden_neighbors_num,b=hidden_neighbor_mine_num))
        for mine_combination in combinations(hidden_neighbors,hidden_neighbor_mine_num):

            print ("the mine we tend to add {}".format(mine_combination))
            if self.insert_fake_mines_into_map_and_check_valid(mine_combination):
                print("We check this combination is valid")
                self.candidate_high_safe_list.append(set(hidden_neighbors).difference(mine_combination))
                print("the probability safe list we get to dig is {}".format(self.candidate_high_safe_list))
            else:
                print("the combinations() is invalid :{}".format(mine_combination))
        remain=random.sample(self.candidate_high_safe_list,1)
        print(remain)
        print(type(self.candidate_cell))
        # self.candidate_cell=random.sample(remain[0],1)[0]
        print("most appear candidate is ")
        self.candidate_cell=self.count_max_appear_node(self.candidate_high_safe_list)
        print(self.candidate_cell)

    def insert_fake_mines_into_map_and_check_valid(self,mines):
        temp_map=copy.deepcopy(self.map)
        for mine in mines :
            temp_map[mine]=MINE
            print("generating fake map")
        flag=True
        while flag:
            flag=False
            for pick in self.picked:
                # print("we check pick is {}".format(pick))
                clue = self.env.query(pick[0], pick[1])
                if clue==NO_CLUE:
                    print("no clue we skip checking this cell")
                    continue
                revealed_mines=self.revealed_mines_for_test(pick,temp_map)
                hidden_nirghbors=self.hidden_neighbors_for_test(pick,temp_map)
                safe_neighbors=self.safe_neighbors_for_test(pick,temp_map)
                if clue-len(revealed_mines)==0:
                    for hidden_nirghbor in hidden_nirghbors:
                        temp_map[hidden_nirghbor]=TEMP_SAFE
                        flag = True

                elif clue-len(revealed_mines)<0:
                    print("Invalid Assumption_________________________________________________")
                    return False
                elif clue-len(revealed_mines)>0:
                    if clue-len(revealed_mines)==len(hidden_nirghbors):
                        for hidden_nirghbor in hidden_nirghbors:
                            temp_map[hidden_nirghbor]=-1
                        flag = True
        return True


    def count_max_appear_node(self,list):
        dict={}
        for set in list:
            for tup in set :
                dict[tup]=0
        for set in list:
            for tup in set :
                dict[tup]=dict[tup]+1
        tp=max(dict,key=dict.get)
        return tp





    def revealed_mines_for_test(self, cell,map):
        res = self.env.neighbors(cell[0], cell[1])
        delt = []
        for i in res:
            if map[i] != MINE:
                delt.append(i)
        for i in delt:
            res.remove(i)
        return res

    def hidden_neighbors_for_test(self, cell,map):
        res = self.env.neighbors(cell[0], cell[1])
        delt = []
        for i in res:
            if map[i] != HIDDEN:
                delt.append(i)
        for i in delt:
            res.remove(i)
        return res
    def safe_neighbors_for_test(self, cell,map):
        res = self.env.neighbors(cell[0], cell[1])
        # print(res)
        delt = []
        for i in res:
            # print(i)
            # print(self.map[i])
            if map[i] < 0: # safe cell is larger than 0
                delt.append(i)
        for i in delt:
            res.remove(i)
        return res
def calculate_average(num):
    sum=0
    for i in range(num):
        mine_map = Env_Noclues.map_possible_noclues(10, 60,0.2)
        agent = Improved_Agent(mine_map)
        agent.run()
        # agent.print_map()
        # agent.pick()
        # agent.pick()
        # agent.print_map()
        agent.show_knowledge()
        score=agent.reveal / agent.env.mines
        sum+=score
        print("score: {}".format(agent.reveal / agent.env.mines))
    print("average {}".format(sum/num))
    return  sum/num

if __name__ == "__main__":
    # mine_map = Env.map(10, 40)
    # agent = Improved_Agent(mine_map)
    # agent.run()
    # # agent.print_map()
    # # agent.pick()
    # # agent.pick()
    # # agent.print_map()
    # agent.show_knowledge()
    # print("score: {}".format(agent.reveal/agent.env.mines))
    calculate_average(20)##10*10 with 60 mines and 0.2 return no clue


from Assignment2.Possible_generate_no_clue_cell.Improved_Agent_Noclues import Improved_Agent
from Assignment2.Possible_generate_no_clue_cell import  Env_Noclues

import copy
HIDDEN = -2
MINE = -1
TEMP_SAFE=100
NO_CLUE=999
class Known_mines(Improved_Agent):
    def __init__(self, env:  Env_Noclues.map):
        Improved_Agent .__init__(self, env)
        self.total_mines=env.mines




    def insert_fake_mines_into_map_and_check_valid(self,mines):
        temp_map=copy.deepcopy(self.map)
        for mine in mines :
            temp_map[mine]=MINE
            print("generating fake map")
        if not self.is_valid_total_number_mines(temp_map):
            print("first check:#mines larger than total mines and we can not add mine using this combination")
            print("Invalid Assumption_________________________________________________")
            return False
        flag=True
        while flag:
            flag=False
            for pick in self.picked:
                # print("we check pick is {}".format(pick))
                clue = self.env.query(pick[0], pick[1])
                if clue == NO_CLUE:
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
                        if not self.is_valid_total_number_mines(temp_map):
                            print(
                                "second check:#mines larger than total mines and we can not add mine using this combination")
                            print("Invalid Assumption_________________________________________________")
                            return False
                        flag = True
        return True
    def is_valid_total_number_mines(self,map):
        measured_total_mines=0
        for i in range(self.dim):
            for j in range(self.dim):
                if map[(i,j)]==-1:
                    measured_total_mines=measured_total_mines+1
        return  measured_total_mines<=self.total_mines


def calculate_average(num):
    sum=0
    for i in range(num):
        mine_map = Env_Noclues.map_possible_noclues(10, 40,0.2)
        agent = Known_mines(mine_map)
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

if __name__=="__main__":
    # mine_map = Env.map(10, 40)
    # agent = Improved_Agent(mine_map)
    # agent.run()
    # # agent.print_map()
    # # agent.pick()
    # # agent.pick()
    # # agent.print_map()
    # agent.show_knowledge()
    # print("score: {}".format(agent.reveal/agent.env.mines))
    calculate_average(20)




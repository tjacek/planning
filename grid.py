import numpy as np 
import search

class GridSearch(search.FowardSearch):
    def __init__(self,grid):
        self.grid=grid
        self.states={}
        self.goal=None

    def __call__(self,start,end):
        if(self.grid[end[0]][end[1]]==1):
            return False	
        self.goal=self.get_state(end)
        start=self.get_state(start)
        super().__call__(start)	

    def is_goal(self,state_i):
        return self.goal.id==state_i.id

    def next_state(self,state_i):
        raise NotImplemented()

    def get_state(self, pair):
        state_id=cantor_paring(pair)
        if(not state_id in self.states):
            self.states[state_id]=search.State(state_id)
        return self.states[state_id]

def cantor_paring(k):
    return (k[0]+k[1])*(k[0]+k[1]+1)/2	

def read_grid(in_path):
    with open (in_path, "r") as grid_file:
        text=[[c_j for c_j in line_i] 
                for line_i in grid_file.read().split('\n')]
        text=np.array(text)
        text[text=='#']='1'
        text[text!='1']='0'
        text=text.astype(int)
        return GridSearch(text)

gs=read_grid("sample.txt")
gs((0,0),(5,3))   
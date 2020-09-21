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
        return super().__call__(start)	

    def is_goal(self,state_i):
        return self.goal.id==state_i.id

    def next_state(self,state_i):
        pair_i=cantor_invert(state_i.id)
        delta=[-1,0,1]
        neigh=[ (pair_i[0]+x,pair_i[1]+y)
                for x in delta
                    for y in delta]
        neigh=[ self.get_state(neig_i)
                for neig_i in neigh
                    if(self.valid(neig_i))]
        return neigh

    def get_state(self, pair):
        state_id=cantor_paring(pair)
        if(not state_id in self.states):
            self.states[state_id]=search.State(state_id)
        return self.states[state_id]
    
    def valid(self,pair):
        if(pair[0]<0 or pair[1]<0):
            return False
        bound=[ value>=bound  
        	        for value,bound in zip(pair,self.grid.shape)]
        if(any(bound)):
        	return False
        return self.grid[pair[0],pair[1]]==0


def cantor_paring(k):
    return (k[0]+k[1])*(k[0]+k[1]+1)/2 + k[1]

def cantor_invert(z):
    w=np.floor( (np.sqrt(8*z+1)-1)/2 )
    t= (w*w+w)/2
    y=z-t
    x=w-y
    return int(x),int(y)

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
print(gs((0,0),(5,3)))
#print(gs.valid((0,0)))
#print(cantor_invert(cantor_paring((3,2))))
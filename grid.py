import numpy as np 
import search

class GridSearch(search.FowardSearch):
    def __init__(self,grid,gen_pairs=None):
        self.grid=grid
        self.states={}
        self.goal=None
        if(not gen_pairs):
            gen_pairs=four_direction
        self.gen_pairs=gen_pairs	

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
        neigh=[ self.get_state(neig_i)
                for neig_i in self.gen_pairs(pair_i)#neigh
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

    def get_plan(self):
        path=[]
        current=self.goal
        while(current):
            path.append(cantor_invert(current.id))
            current=current.parent
        path.reverse()
        return path

    def get_grid(self):
        text=self.grid.astype(str)
        text[text=='0']='.'
        text[text=='1']='#'
        return text	

class AllDirections(object):
    def __init__(self):
        self.delta=[-1,0,1]
    
    def __call__(self,pair_i): 	
        return [(pair_i[0]+x,pair_i[1]+y)
                for x in self.delta
                    for y in self.delta
                        if(x!=0 and y!=0)]

def four_direction(pair_i):
    x,y=pair_i
    return [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]	

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

def save_plan(grid_search,out_path=None):
    grid=grid_search.get_grid()
    plan=grid_search.get_plan()
    for pair_i in plan:
        grid[pair_i]='@'
    text='\n'.join([''.join(row) 
    	                for row in grid])
    if(out_path):
        with open(out_path, "w") as text_file:
            text_file.write(text)
    else:
        print(text)	

gs=read_grid("sample.txt")
print(gs((0,0),(0,20)))
save_plan(gs)#,"plan.txt")
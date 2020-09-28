import numpy as np
import foward

class GridStates(object):
    def __init__(self,grid,queue=None,gen_pairs=None,):
        self.grid=grid
        self.states={}
        self.goal=None
        if(not gen_pairs):
            gen_pairs=four_direction
        self.gen_pairs=gen_pairs    	
    
    def is_goal(self,state_i):
        return self.goal.id==state_i.id

    def next_state(self,state_i):
        pair_i=cantor_invert(state_i.id)
        neigh=[ self.get_state(neig_i)
                for neig_i in self.gen_pairs(pair_i)#neigh
                    if(self.grid.valid(neig_i))]
        return neigh

    def get_state(self, pair):
        state_id=cantor_paring(pair)
        if(not state_id in self.states):
            self.states[state_id]=foward.State(state_id)
        return self.states[state_id]

def distance_heuristic(state_i,goal):
    pair_i=cantor_invert(state_i.id)
    goal=cantor_invert(goal.id)
    return sum([np.abs(x-y) for x,y in zip(pair_i,goal)])

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
import sys
sys.path.append("..")
import numpy as np
import collision

class Grid(object):
    def __init__(self):	
        self.vertices={}
        self.illegal=set()

    def add_state(self,triple_i,position):
        x,y,z=triple_i
        near=[(x-1,y,z),(x,y-1,z),(x,y,z-1)]
        edges=[]
        for near_i in near:
            if(all([cord_j>0 for cord_j in near_i])):
                id_i=get_id(near_i)
                if(not id_i in self.illegal):
                	edges.append(self.vertices[id_i])
        new_vertex=Vertex(position)
        for vertex_i in edges:
            vertex_i.add_edge(new_vertex)
            new_vertex.add_edge(vertex_i)
        self.vertices[get_id(triple_i)]=new_vertex
    
    def add_illegal(self,triple_i):
        self.illegal.update([get_id(triple_i)])	

    def get_positions(self):
        return [vert_i.position 
                for vert_i in self.vertices.values()] 	

    def non_isolated(self):
        self.vertices={ id_i:vertex_i
                        for id_i,vertex_i in self.vertices.items()
                            if( len(vertex_i.edges) >0)} 	

    def find_close(self,position):
        states=list(self.vertices.values())
        distance=[collision.polygon_metric(state_i.position,position)
                    for state_i in states]
        return states[np.argmax(distance)]

    def dijkstra(self,start,end):
        states=list(self.vertices.values())
        for state_i in states:
        	state_i.reset()
        start.cost=0
        while(states):
            states.sort(key=lambda x:x.cost,reverse=True)
            state_i=states.pop()
            for near_j in state_i.edges:
            	if(near_j.cost>(state_i.cost+1)):
                    near_j.cost=state_i.cost+1
                    near_j.parent=state_i	
        positions=[]
        state_i=end
        while(state_i):
            positions.append(state_i.position)
            state_i=state_i.parent
        return positions

class Vertex(object):
    def __init__(self,position):
        self.position=position
        self.edges=[]
        self.visited=False
        self.parent=None
        self.cost=np.inf

    def add_edge(self,vertex):
        self.edges.append(vertex)

    def reset(self):
        self.visited=False
        self.parent=None
        self.cost=np.inf	

def grid_search(problem,bounds):
    grid=make_grid(problem,bounds)
    start=grid.find_close(problem.start)
    end=grid.find_close(problem.end)
    return grid.dijkstra(start,end)
    
def make_grid(problem,bounds):
    if(type(bounds)==int):
        x,y,z=bounds,bounds,bounds
    else:
        x,y,z=bounds 	
    min_point,width,height=problem.get_box().as_point()
    step_theta,step_x,step_y=2*np.pi/x,width/y,height/z
    grid=Grid()
    for i in range(x):
        for j in range(y+1):
            for k in range(z+1):
                point_ijk=(i*step_theta,j*step_x,k*step_y) #(i*step_x,j*step_y,k*step_theta)
                position_ijk=problem.legal_position(point_ijk)
                triple_i=(i,j,k)
                if(position_ijk):
                    grid.add_state(triple_i,position_ijk)
                else:
                    grid.add_illegal(triple_i)
    grid.non_isolated()
    return grid

def get_id(triple):
	x,y,z=triple
	left=cantor_paring((x,y))
	return cantor_paring((left,z))

def get_triple(id):
    left,z=cantor_invert(id)
    x,y=cantor_invert(left)
    return x,y,z

def cantor_paring(k):
    return (k[0]+k[1])*(k[0]+k[1]+1)/2 + k[1]

def cantor_invert(z):
    w=np.floor( (np.sqrt(8*z+1)-1)/2 )
    t= (w*w+w)/2
    y=z-t
    x=w-y
    return int(x),int(y)

import world2D,plot
problem=world2D.read_problem("square.json")
#position=make_grid(problem,(5,5,5)).get_positions()
position=grid_search(problem,(5,5,5))
plot.plot_problem(problem,position,False)
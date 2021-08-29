import sys
sys.path.append("..")
import numpy as np
import collision,states

class Grid(object):
    def __init__(self):	
        self.vertices={}
        self.illegal=set()

    def add_state(self,triple_i,state):
        x,y,z=triple_i
        near=[(x-1,y,z),(x,y-1,z),(x,y,z-1)]
        edges=[]
        for near_i in near:
            if(all([cord_j>0 for cord_j in near_i])):
                id_i=get_id(near_i)
                if(not id_i in self.illegal):
                	edges.append(self.vertices[id_i])
        new_vertex=Vertex(state)
        for vertex_i in edges:
            vertex_i.add_edge(new_vertex)
            new_vertex.add_edge(vertex_i)
        self.vertices[get_id(triple_i)]=new_vertex
        return new_vertex

    def add_illegal(self,triple_i):
        self.illegal.update([get_id(triple_i)])	

    def get_positions(self):
        return [vert_i.position 
                for vert_i in self.vertices.values()] 	

    def non_isolated(self):
        self.vertices={ id_i:vertex_i
                        for id_i,vertex_i in self.vertices.items()
                            if( len(vertex_i.edges) >0)} 	

    def find_close(self,state):
        vertices=list(self.vertices.values())
        distance=[states.polygon_metric(vert_i.state,state)
                    for vert_i in vertices]
        return vertices[np.argmax(distance)]

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
        states=[]
        vertex_i=end
        while(vertex_i):
            states.append(vertex_i.state)
            vertex_i=vertex_i.parent
        print(len(states))
        return states

class Vertex(object):
    def __init__(self,state):
        self.state=state
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
    min_point,width,height=problem.get_bounds()
    step_theta,step_x,step_y=2*np.pi/x,width/y,height/z
    grid=Grid()
    for i in range(x):
        for j in range(y+1):
            for k in range(z+1):
                point_ijk=(i*step_theta,j*step_x,k*step_y)
                position_ijk=problem.legal_position(point_ijk)
                triple_i=(i,j,k)
                state_ijk=states.State(point_ijk,position_ijk)
                if(position_ijk):
                    grid.add_state(triple_i,state_ijk)
                else:
                    grid.add_illegal(triple_i)
    grid.non_isolated()
    return grid

def get_id(triple):
	x,y,z=triple
	left=cantor_paring((x,y))
	return cantor_paring((left,z))

def cantor_paring(k):
    return (k[0]+k[1])*(k[0]+k[1]+1)/2 + k[1]

#import world2D,plot
#problem=world2D.read_problem("square.json")
#position=make_grid(problem,(5,5,5)).get_positions()
#position=grid_search(problem,(5,7,7))
#plot.plot_problem(problem,position,False)
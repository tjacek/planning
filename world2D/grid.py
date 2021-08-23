import sys
sys.path.append("..")
import numpy as np

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

class Vertex(object):
    def __init__(self,position):
        self.position=position
        self.edges=[]

    def add_edge(self,vertex):
        self.edges.append(vertex)

def make_grid(problem,bounds):
    if(type(bounds)==int):
        x,y,z=bounds,bounds,bounds
    else:
        x,y,z=bounds 	
    min_point,width,height=problem.get_box().as_point()
    step_theta,step_x,step_y=2*np.pi/x,width/y,height/z
    grid=Grid()
    for i in range(x):
        for j in range(y):
            for k in range(z):
                point_ijk=(i*step_x,j*step_y,k*step_theta)
                position_ijk=problem.legal_position(point_ijk)
                triple_i=(i,j,k)
                if(position_ijk):
                    grid.add_state(triple_i,position_ijk)
                else:
                    grid.add_illegal(triple_i)
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
grid=make_grid(problem,(5,5,5))
plot.plot_problem(problem,grid.get_positions(),False)
import pygame as pg
import numpy as np
import grid

class GridGraph(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def __call__(self,start_cord,goal_cord):
        start,goal=self[start_cord],self[goal_cord]
        self.dijkstra(goal)
        path=[]
        vertex_i=start
        while(vertex_i):
            path.append(vertex_i)
            vertex_i=vertex_i.parent
        print(len(path))
        return path

    def __getitem__(self,cord):
        return self.vertices[cantor_paring(cord)]	

    def dijkstra(self,end):
        self.reset()
        states=list(self.vertices.values())
        end.cost=0
        while(states):
            states.sort(key=lambda x:x.cost,reverse=True)
            state_i=self[states.pop().cord]
            for near_j in state_i.edges:
            	near_j=self[near_j]
            	if(near_j.cost>(state_i.cost+1)):
                    near_j.cost=state_i.cost+1
                    near_j.parent=state_i

    def reset(self):
        for vertex_i in self.vertices.values():
            vertex_i.reset()	

class Vertex(object):
    def __init__(self,cord,edges=[]):
        self.cord=cord
        self.edges=edges
        self.visited=False
        self.parent=None
        self.cost=np.inf

    def reset(self):
        self.visited=False
        self.parent=None
        self.cost=np.inf	

class SearchContoler(object):
    def __init__(self,grid,graph_grid,goal):
        self.grid=grid
        self.graph_grid=graph_grid
        self.goal=goal
        self.path=None
        self.mode=True

    def on_click(self,point):
        if(self.grid.colide(point)):
            if(self.mode):
                self.set_start(point)
            else:
                self.set_goal(point)

    def on_key(self,key):
        self.mode=not self.mode
        print(self.mode)

    def set_start(self,point):
        self.reset_path()
        start=self.grid.get_cord(point)
        path=self.graph_grid(start,self.goal)
        for state_i in path:
            color_i=grid.CellColors.path
            self.grid.set_color(state_i.cord,color_i)
        self.path=path        
    
    def set_goal(self,point):
        self.reset_path()
        self.grid.set_color(self.goal,grid.CellColors.empty)
        self.goal=self.grid.get_cord(point)
        color_i=grid.CellColors.path
        self.grid.set_color(self.goal,color_i)

    def reset_path(self):
        if(self.path):
            for state_i in self.path:
                color_i=grid.CellColors.empty
                self.grid.set_color(state_i.cord,color_i)	

def get_grid_graph(raw_grid):
    vertices={}
    for i in range(raw_grid.x):
        for j in range(raw_grid.y):
            cord=(i,j)
            key_ij=cantor_paring(cord)
            vertex_ij=Vertex(cord,raw_grid.near(*cord))
            vertices[key_ij]=vertex_ij
    return GridGraph(vertices)	

def search(in_path,goal=(9,7),step=40):
    raw_grid=grid.read_grid(in_path,step)	
    graph_grid=get_grid_graph(raw_grid)
#    graph_grid((2,2),(9,7))
    raw_grid.set_color(goal,grid.CellColors.goal)
    controler=SearchContoler(raw_grid,graph_grid,goal)
    grid.grid_loop(controler)

def cantor_paring(k):
    return (k[0]+k[1])*(k[0]+k[1]+1)/2 + k[1]

search("test.txt")
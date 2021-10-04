import pygame as pg
import grid,graph,foward

class SearchContoler(object):
    def __init__(self,grid,graph_grid,goal=(0,0)):
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
        path=self.graph_grid.find_path(start)
        if(not path):
            return
        for state_i in path:
            self.grid.set_color(state_i.cord,"path")
        self.path=path        
    
    def set_goal(self,point):
        self.reset_path()
        if(self.goal):
            self.grid.set_color(self.goal,"empty")
        self.goal=self.grid.get_cord(point)
        self.graph_grid.set_goal(self.goal)
        self.grid.set_color(self.goal,"goal")

    def reset_path(self):
        if(self.path):
            for state_i in self.path:
                self.grid.set_color(state_i.cord,"empty")

def search(in_path,step=40):
    raw_grid=grid.read_grid(in_path,step)	
    vertices=graph.get_grid_graph(raw_grid)
    graph_grid=graph.DijkstraSearch(vertices)
#    graph_grid=foward.FowardSearch(vertices,foward.BestFirst)
    controler=SearchContoler(raw_grid,graph_grid)
    controler.set_goal((3,3))
    grid.grid_loop(controler)

search("test.txt")
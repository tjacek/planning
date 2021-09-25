import pygame as pg
import grid,graph

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
        for state_i in path:
            color_i=grid.CellColors.path
            self.grid.set_color(state_i.cord,color_i)
        self.path=path        
    
    def set_goal(self,point):
        self.reset_path()
        if(self.goal):
            self.grid.set_color(self.goal,grid.CellColors.empty)
        self.goal=self.grid.get_cord(point)
        self.graph_grid.set_goal(self.goal)
        color_i=grid.CellColors.goal
        self.grid.set_color(self.goal,color_i)

    def reset_path(self):
        if(self.path):
            for state_i in self.path:
                color_i=grid.CellColors.empty
                self.grid.set_color(state_i.cord,color_i)

def search(in_path,step=40):
    raw_grid=grid.read_grid(in_path,step)	
    vertices=graph.get_grid_graph(raw_grid)
    graph_grid=graph.DijkstraSearch(vertices)
    controler=SearchContoler(raw_grid,graph_grid)
    controler.set_goal((3,3))
    grid.grid_loop(controler)

search("test.txt")
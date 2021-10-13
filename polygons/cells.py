import numpy as np
import pygame as pg
import polygons,draw

class CellControler(draw.DrawControler):
    def __init__(self,world,event,cells):
        super().__init__(world)
        self.event=event
        self.cells=cells

    def show(self,window):
        window.fill((0,0,0))
        for x_i in self.event:
            pg.draw.line(window,(0,0,128),(x_i,0),(x_i,800))
        for point_i in self.cells:
            pg.draw.circle(window,(128,0,0), point_i, 5)
        self.world.show(window)

class Edge(object):
    def __init__(self,start,end):
        if(start[0]>end[0]):
            start,end=end,start
        self.start=start
        self.end=end

    def __call__(self,x):
        if(self.start[0]<x and x<self.end[0]):
            a=(self.start[1]-self.end[1])/(self.start[0]-self.end[0])
            b=self.end[1]-a* self.end[0]
            return [x,a*x+b]
        return None

def vertex_decomp(world):
    w_max=world.get_box()[1]
    bounds=(0,w_max[1])
    event=world.vertices()[0]
    event.sort()
    edges=get_edges(world)
    all_cells=[]
    for event_i in event:
        all_cells+=find_cells(event_i,edges,bounds)
    return all_cells,event

def find_cells(event_i,edges,bounds):
    upper,lower=[],[]
    for edge_j in edges:
        point_ij=edge_j(event_i)
        if(point_ij):
            if(point_ij[0]<event_i):
                lower.append(point_ij)
            else:
                upper.append(point_ij)
    upper.sort(key=lambda x:x[1],reverse=True)
    lower.sort(key=lambda x:x[1])#,reverse=True)
    if(upper):
        start=upper[0]
    else:
        start=(event_i,bounds[0])
    if(lower):
        end=lower[-1]
    else:
        end=(event_i,bounds[1])
    print(start)
    print(lower)
    return [start,end]

def get_edges(world):
    edges=[]
    for pol_i in world.polygons:
        for edge_j in pol_i.get_edges():
            edges.append(Edge(*edge_j))
    return edges

world=polygons.read_world("test.txt")
cells,event=vertex_decomp(world)
control=CellControler(world,event,cells)
#control.points=cells
draw.polygon_loop(control)
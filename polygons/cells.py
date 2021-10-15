import numpy as np
import pygame as pg
import polygons,draw,event

class CellControler(draw.DrawControler):
    def __init__(self,world,event,cells):
        super().__init__(world)
        self.event=event
        self.cells=cells

    def show(self,window):
        window.fill((0,0,0))
        self.world.show(window)
        for x_i in self.event:
            pg.draw.line(window,(0,0,128),(x_i,0),(x_i,800))
        for point_i in self.cells:
            pg.draw.circle(window,(128,0,0), point_i, 5)

class EdgeControler(object):
    def __init__(self,world,edges,points):
        self.world=world
        self.edges=edges
        self.points=points

    def show(self,window):
        window.fill((0,0,0))
#        self.world.show(window)
        for edge_i in self.edges:
            pg.draw.line(window,(0,0,128),edge_i.start,edge_i.end)
        for point_i in self.points:
            pg.draw.circle(window,(128,0,0), point_i, 5)

class Edge(object):
    def __init__(self,start,end):
        if(start[0]>end[0]):
            start,end=end,start
        alpha,length=to_polar(start,end)
        self.start=start
        self.end=end
        self.alpha=alpha
        self.length=length

    def __call__(self,event):        
        if(self.start[0]<event[0] and event[0]<self.end[0]):
            x=event[0]
            k=(x-self.start[0])/(self.length*np.cos(self.alpha))
            y=self.start[1] + k*self.length*np.sin(self.alpha)
            return (x,y)
        return None

class Extend(object):
    def __init__(self,edges,bounds):
        self.edges=edges
        self.bounds=bounds

    def __call__(self,x,lower=False):
        critical=[]
        for edge_i in self.edges:
            point_i=edge_i(x)
            if(point_i):
                cond= point_i[1]<x[1]
                if(lower):
                    cond=not cond
                if(cond):
                    critical.append(point_i)
        if(not critical):
            return self.not_found(x,lower)
        else:
            critical.sort(key=lambda x:x[1],reverse=lower)
            return [critical[-1]]
        
    def not_found(self,vertex,lower):
        x=vertex[0]
        if(lower):
            y=self.bounds[1]
        else:
            y=self.bounds[0]
        return [(x,y)]

def to_polar(start,end):
    diff=np.array(end)-np.array(start)
    alpha=np.arctan(diff[1]/diff[0])
    length=np.linalg.norm(diff)
    return alpha,length

def vertex_decomp(world):
    edges,events= get_data(world)
    events.sort(key=lambda x:x.vertex[0])
    w_max=world.get_box()[1]
    bounds=(0,w_max[1]+30)
    extend=Extend(edges,bounds)
    critical=event.get_critical(events,extend)
    print(len(edges))
    print(len(critical))
    lines=[event_i.vertex[0] for event_i in events]
    return critical,lines

def get_data(world):
    edges=[]
    for pol_i in world.polygons:
        for edge_j in pol_i.get_edges():
            edges.append(Edge(*edge_j))
    return edges,event.get_events(world)

if __name__ == "__main__":
    world=polygons.read_world("test.txt")
    cells,events=vertex_decomp(world)
#    control=EdgeControler(world,edges,points) 
    control=CellControler(world,events,cells)
#    control.points=cells
    draw.polygon_loop(control)
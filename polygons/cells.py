import numpy as np
import pygame as pg
import polygons,draw,event

class CellControler(draw.DrawControler):
    def __init__(self,world,lines,cells,vertex):
        super().__init__(world)
        self.lines=lines
        self.cells=cells
        self.vertex=vertex

    def show(self,window):
        window.fill((0,0,0))
        self.world.show(window)
        for x_i in self.lines:
            pg.draw.line(window,(0,0,128),(x_i,0),(x_i,800))
        for point_i in self.cells:
            pg.draw.circle(window,(128,0,0), point_i, 5)
        for point_i,type_i in self.vertex:
            print(point_i)
            print(type(type_i))
            pg.draw.circle(window,type_i, point_i, 5)

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

def vertex_decomp(world):
    events,edges= event.get_events(world)
    events.sort(key=lambda x:x.vertex[0])
    w_max=world.get_box()[1]
    bounds=(0,w_max[1]+30)
    extend=Extend(edges,bounds)
    critical=event.get_critical(events,extend)
    lines=[event_i.vertex[0] for event_i in events]
#    critical+=[event_i.vertex for event_i in events]
    vertex=[(event_i.vertex,event_i.get_type().value) 
        for event_i in events]
#    raise Exception(vertex)
    return critical,lines,vertex

if __name__ == "__main__":
    world=polygons.read_world("test.txt")
    cells,lines,vertex =vertex_decomp(world)
    print(vertex)
    control=CellControler(world,lines,cells,vertex)
    draw.polygon_loop(control)
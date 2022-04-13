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
    critical+=[event_i.vertex for event_i in events]
    return critical,lines

if __name__ == "__main__":
    world=polygons.read_world("test.txt")
    cells,events=vertex_decomp(world)
#    control=EdgeControler(world,edges,points) 
    control=CellControler(world,events,cells)
#    control.points=cells
    draw.polygon_loop(control)
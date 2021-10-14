import numpy as np
import pygame as pg
import polygons,draw

class EventControler(draw.DrawControler):
    def __init__(self,world,event):
        super().__init__(world)
        self.event=event

    def show(self,window):
        window.fill((0,0,0))
        self.world.show(window)
        for event_i in self.event:
            pg.draw.circle(window,(128,0,0),event_i.vertex,5)        

class Event(object):
    def __init__(self,vertex,in_edge,out_edge):
        self.vertex=vertex
        self.in_edge =in_edge
        self.out_edge=out_edge

def get_events(world):
    events=[]
    for pol_i in world.polygons:
        edges_i=pol_i.get_edges()
        size=len(edges_i)	
        for j in range(0,size):
            print(j)
            in_edge=edges_i[j-1]
            out_edge=edges_i[j]
            vertex=in_edge[1]
            events.append(Event(vertex,in_edge,out_edge))
    return events

world=polygons.read_world("test.txt")
events=get_events(world)
control=EventControler(world,events)
draw.polygon_loop(control)

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
            color_i= event_i.get_type()
            pg.draw.circle(window,color_i,event_i.vertex,5)        

class Event(object):
    def __init__(self,vertex,in_edge,out_edge):
        self.vertex=vertex
        self.in_edge =in_edge
        self.out_edge=out_edge

    def get_type(self):
        all_on_right=(self.vertex[0]<self.out_edge[0]
                and self.vertex[0]<self.in_edge[0])
        all_on_left=(self.vertex[0]>self.out_edge[0]
                and self.vertex[0]>self.in_edge[0])
        orient_y=(self.out_edge[1]<self.in_edge[1] )
        if( (orient_y and all_on_right) or
              (not orient_y and all_on_left)):
            return (128,0,0)
        if( (not orient_y and all_on_right) or
              (orient_y and all_on_left)):
            return (0,0,128)
        orient_x=(self.out_edge[0]<self.in_edge[0])
        if(orient_x):
            return (0,128,128)
        else:
            return (128,128,0)


def get_events(world):
    events=[]
    for pol_i in world.polygons:
        edges_i=pol_i.get_edges()
        size=len(edges_i)	
        for j in range(0,size):
            print(j)
            in_edge=edges_i[j-1][0]
            out_edge=edges_i[j][1]
            vertex=edges_i[j-1][1]
            events.append(Event(vertex,in_edge,out_edge))
    return events

world=polygons.read_world("test.txt")
events=get_events(world)
control=EventControler(world,events)
draw.polygon_loop(control)

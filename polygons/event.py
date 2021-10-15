import numpy as np
import pygame as pg
from enum import Enum
import polygons,draw

class EventType(Enum):
    two_extend=(128,0,0)
    zero_extend=(0,0,128)
    upper=(0,128,128)
    lower=(128,128,0)

class EventControler(draw.DrawControler):
    def __init__(self,world,event):
        super().__init__(world)
        self.event=event

    def show(self,window):
        window.fill((0,0,0))
        self.world.show(window)
        for event_i in self.event:
            color_i= event_i.get_type().value
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
            return EventType.zero_extend
        if( (not orient_y and all_on_right) or
              (orient_y and all_on_left)):
            return EventType.two_extend
        orient_x=(self.out_edge[0]<self.in_edge[0])
        if(orient_x):
            return EventType.upper
        else:
            return EventType.lower

def get_critical(events,extend):
    critical_points=[]
    for event_i in events:
        type_i=event_i.get_type()
        if(type_i==EventType.upper):
            critical_points+=extend(event_i.vertex,False)
        if(type_i==EventType.lower):
            critical_points+=extend(event_i.vertex,True)
        if(type_i==EventType.two_extend):
            critical_points+=extend(event_i.vertex,False)
            critical_points+=extend(event_i.vertex,True)
    return critical_points

def get_events(world):
    events=[]#,[]
    for pol_i in world.polygons:
        edges_i=pol_i.get_edges()
        size=len(edges_i)	
        for j in range(0,size):
            in_edge=edges_i[j-1][0]
            out_edge=edges_i[j][1]
            vertex=edges_i[j-1][1]
            events.append(Event(vertex,in_edge,out_edge))
    return events#,edges

if __name__ == "__main__":
    world=polygons.read_world("test.txt")
    events=get_events(world)
    control=EventControler(world,events)
    draw.polygon_loop(control)
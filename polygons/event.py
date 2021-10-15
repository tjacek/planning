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
    events,edges=get_events(world)
    events.sort(key=lambda x:x.vertex[0])
    critical_points=[]
    for event_i in events:
        type_i=event_i.get_type()
        if(type_i==EventType.upper):
            critical_points+=extend(event_i.vertex,edges)
        if(type_i==EventType.lower):
            critical_points+=extend(event_i.vertex,edges,w_max[1],True)
        if(type_i==EventType.two_extend):
            critical_points+=extend(event_i.vertex,edges)
            critical_points+=extend(event_i.vertex,edges,w_max[1],True)
    x=[event_i.vertex[0] for event_i in events]
    return critical_points,x

def get_events(world):
    events,edges=[],[]
    for pol_i in world.polygons:
        edges_i=pol_i.get_edges()
        size=len(edges_i)	
        for j in range(0,size):
            in_edge=edges_i[j-1][0]
            out_edge=edges_i[j][1]
            vertex=edges_i[j-1][1]
            events.append(Event(vertex,in_edge,out_edge))
            edges.append(Edge(in_edge,out_edge))
    return events,edges

def extend(vertex,edges,bound=0,lower=False):
    upper=[]
    for edge_i in edges:
        point_i=edge_i(vertex[0])
        if(point_i):
            cond= point_i[1]<vertex[1]
            if(lower):
                cond=not cond
            if(cond):
                upper.append(point_i)
    if(not upper):
        return [(vertex[0],bound)]
    else:
        upper.sort(key=lambda x:x[1],reverse=lower)
#        if(lower):
        return [upper[-1]]
#        else:
#            return [upper[-1]]

world=polygons.read_world("test.txt")
points,events=vertex_decomp(world)
print(len(points))
import cells
control=cells.CellControler(world,events,points)
#events,edges=get_events(world)
#control=EventControler(world,events)
draw.polygon_loop(control)
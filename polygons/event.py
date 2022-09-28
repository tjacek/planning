
import numpy as np
import pygame as pg
from enum import Enum
import polygons,draw

class EventType(Enum):
    two_extend=(128,0,128)
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
        self.type=None

    def get_type(self):
        if(self.type is None):
            self.type=self.compute_type()
        return self.type

    def compute_type(self):
        all_on_right=(self.vertex[0]<self.out_node()[0]
            and self.vertex[0]<self.in_node()[0])
        all_on_left=(self.vertex[0]>self.out_node()[0]
            and self.vertex[0]>self.in_node()[0])
        orient_y=(self.out_node()[1]<self.in_node()[1] )
        if( (orient_y and all_on_right) or
              (not orient_y and all_on_left)):
            return EventType.zero_extend
        if( (not orient_y and all_on_right) or
              (orient_y and all_on_left)):
            return EventType.two_extend
        orient_x=(self.out_node()[0]<self.in_node()[0])
        if(orient_x):
            return EventType.upper
        else:
            return EventType.lower

    def out_node(self):
        if(self.out_edge.orient):
            return self.out_edge.end
        else:
            return self.out_edge.start

    def in_node(self):
        if(self.in_edge.orient):
            return self.in_edge.start
        else:
            return self.in_edge.end

class Edge(object):
    def __init__(self,start,end):
        if(start[0]>end[0]):
            start,end=end,start
            self.orient=False
        else:
            self.orient=True
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

def to_polar(start,end):
    diff=np.array(end)-np.array(start)
    alpha=np.arctan(diff[1]/diff[0])
    length=np.linalg.norm(diff)
    return alpha,length

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
    events,edges=[],[]
    for pol_i in world.polygons:
        edges_i=pol_i.get_edges()
        size=len(edges_i)	
        for j in range(0,size):
            vertex=edges_i[j-1][1]
            in_edge=Edge(*edges_i[j-1])
            out_edge=Edge(*edges_i[j])
            edges+=[in_edge,out_edge]
            events.append(Event(vertex,in_edge,out_edge))
    return events,edges

if __name__ == "__main__":
    world=polygons.read_world("test.txt")
    events,edges=get_events(world)
    control=EventControler(world,events)
    draw.polygon_loop(control)
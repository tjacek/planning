import numpy as np
import pygame as pg
import polygons,draw,event

class EdgeControler(object):
    def __init__(self,world,sweep):
        self.world=world
        self.sweep=sweep
    
    def on_key(self,key):
        self.sweep()

    def show(self,window):
        window.fill((0,0,0))
        for edge_i in list(self.sweep.edges):
            pg.draw.line(window,(0,0,128),edge_i.start,edge_i.end)

class SweepLine(object):
    def __init__(self,events):
        events.sort(key=lambda x:x.vertex[0],reverse=True)
        self.events=events
        self.edges=set()

    def __call__(self):
        if(self.events):
            event_i=self.events.pop()
            if(event_i.vertex[0]<event_i.out_node()[0]):
                self.edges.update([event_i.out_edge])
            else:
                if(event_i.out_edge in self.edges):
                    self.edges.remove(event_i.out_edge)
            if(event_i.vertex[0]<event_i.in_node()[0]):
                self.edges.update([event_i.in_edge])
            else:
                if(event_i.in_edge in self.edges):
                    self.edges.remove(event_i.in_edge)
            print(len(self.edges))
            return True
        else:
            return None 

world=polygons.read_world("test.txt")
events,edges= event.get_events(world)
sweep=SweepLine(events)
control=EdgeControler(world,sweep)
draw.polygon_loop(control)



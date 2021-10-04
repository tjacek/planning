import numpy as np
import pygame as pg

class World(object):
    def __init__(self,polygons):
        self.polygons=polygons

    def show(self,window):
        for pol_i in self.polygons:
            pol_i.show(window)	

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def show(self,window):
    	pg.draw.polygon(window,(0,128,0),self.vertices)

def make_world():
    pol1=Polygon([[100,100],[200,100],[200,200],[100,200]])
    pol2=Polygon([[300,300],[400,300],[400,400],[300,400]])
    return World([pol1,pol2])

def polygon_loop(world):
    pg.init()
    window = pg.display.set_mode((1000, 1000))
    clock = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        world.show(window)
        pg.display.flip()
        clock.tick(3)
    pg.quit()
    exit()
    
world=make_world()
polygon_loop(world)
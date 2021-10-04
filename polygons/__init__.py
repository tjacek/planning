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

if __name__ == "__main__":
    import gen
    world=gen.gen_world(15)
    polygon_loop(world)
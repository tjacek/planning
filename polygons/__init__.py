import numpy as np
import pygame as pg

class World(object):
    def __init__(self,polygons):
        self.polygons=polygons

    def move(self,motion):
        if(type(motion)==list):
            for motion_i,pol_i in zip(motion,self.polygons):
                pol_i.move(motion_i)
        else:
            for pol_i in self.polygons:
                pol_i.move(motion)

    def show(self,window):
        for pol_i in self.polygons:
            pol_i.show(window)	

class Polygon(object):
    def __init__(self,vertices):
        if(type(vertices)==list):
            vertices=np.array(vertices)
        self.vertices=vertices
    
    def move(self,motion):
        self.vertices=np.array([motion(vert_i)
             for vert_i in self.vertices])

    def show(self,window):
        point=[vert_i for vert_i in self.vertices]
        pg.draw.polygon(window,(0,128,0),point)

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.theta=theta    
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)#+self.b

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
    world=gen.cell_world(30)
    polygon_loop(world)
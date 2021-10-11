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

    def get_box(self):
        raw=[pol_i.get_box() 
                for pol_i in self.polygons]
        raw=list(zip(*raw))
        p_min=np.amin(raw[0],axis=0)
        p_max=np.amax(raw[1],axis=0)
        return (p_min,p_max)

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

    def get_box(self):
        v_min=np.amin(self.vertices,axis=0)
        v_max=np.amax(self.vertices,axis=0)
        return [v_min,v_max]

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.theta=theta    
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b

class SimpleControler(object):
    def __init__(self,world):
        self.world=world

    def on_click(self,point):
        print(point)

    def on_key(self,key):
        print(key)

def polygon_loop(world):
    pg.init()
    a_max=world.get_box()[1]
    bounds=(int(a_max[0]), int(a_max[1]))
    print(bounds)
    window = pg.display.set_mode(bounds)
    clock = pg.time.Clock()
    run = True
    controler=SimpleControler(world)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                controler.on_click(point)
            if event.type == pg.KEYDOWN:
                controler.on_key(event.key)
        controler.world.show(window)
        pg.display.flip()
        clock.tick(3)
    pg.quit()
    exit()

if __name__ == "__main__":
    import gen
    world=gen.cell_world(5)
    polygon_loop(world)
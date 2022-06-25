import pygame as pg
from enum import Enum 
import geometry

class Problem(object):
    def __init__(self,world=None,start=None,end=None):
        if(world is None):
            world=geometry.World()
        self.world=world
        self.start=start
        self.end=end

    def posed(self):
        return (self.start and self.end)

    def show(self,window):
        if(self.start):
            pg.draw.circle(window,(0,64,64), self.start, 5)
        if(self.end):
            pg.draw.circle(window,(64,0,64), self.end, 5)   
        if(self.posed()):
            pg.draw.line(window,(255,255,0),self.start,self.end)
            self.check(window)

    def check(self,window):
        if(len(self.world)>0):
            line=(self.start,self.end)
            for polygon_i in self.world.polygons:
                col_segms=polygon_i.colision(line)
                for segm_j in col_segms:
                    pg.draw.circle(window,(255,0,0),segm_j[0],5)
                    pg.draw.circle(window,(255,0,0),segm_j[1],5)


class EditorMode(Enum):
    OBSTACLE = 1
    START = 2
    END = 3

class Editor(object):
    def __init__(self):
        self.problem=Problem()
        self.points=[]
        self.mode=EditorMode.OBSTACLE
    
    def on_click(self,point):
        if(self.mode==EditorMode.OBSTACLE):
            self.points.append(point)
            print(len(self.points))	
        if(self.mode==EditorMode.START):
            self.problem.start=point
        if(self.mode==EditorMode.END):
            self.problem.end=point

    def on_key(self,key):
        print(key)
        if(key==115):
            self.mode=EditorMode.START
        elif(key==101):
            self.mode=EditorMode.END
        else:
            self.mode=EditorMode.OBSTACLE
            if(len(self.points)>2):
                self.problem.world.add_polygon(self.points)
                self.points.clear()

    def show(self,window):
        window.fill((0,0,0))
        self.problem.show(window)
        for point_i in self.points:
            pg.draw.circle(window,(0,0,128), point_i, 5)
        self.problem.world.show(window)

def editor_loop(bounds=(512,512)):
    obs=Editor()
    pg.init()
    window = pg.display.set_mode(bounds)
    clock = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run=False
            if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                obs.on_click(point)
            if event.type == pg.KEYDOWN:
                obs.on_key(event.key)
        obs.show(window)
        pg.display.flip()
        clock.tick(3)
    obs.problem.world.save("test.json")
    pg.quit()

editor_loop()
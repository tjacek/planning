import pygame as pg
from enum import Enum 
import sys
import world#,geometry

def show_segments(window,segments):
    for segm_i in segments:
        x,y=segm_i
        pg.draw.line(window,(255,255,0),x,y,width=10)

def show_points(window,points):
    for point_i in points:
        pg.draw.circle(window,(255,255,0),point_i,5)

class EditorMode(Enum):
    OBSTACLE = 1
    START = 2
    END = 3
    REMOVE = 4

class Editor(object):
    def __init__(self,problem):
        self.problem=problem#world.Problem()
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
        if(self.mode==EditorMode.REMOVE):
            if(len(self.points)>0):
                pol_i=self.problem.world.inside(self.points[-1])
                if(pol_i):
                    pol_i.rotate(1.0)
                self.points.clear()

    def on_key(self,key):
        print(key)
        if(key==115):
            self.mode=EditorMode.START
        elif(key==101):
            self.mode=EditorMode.END
        elif(key==114):
            self.mode=EditorMode.REMOVE
        else:
            self.mode=EditorMode.OBSTACLE
            if(len(self.points)>2):
                self.problem.world.add_polygon(self.points)
                self.points.clear()

    def show(self,window):
        window.fill((0,0,0))
        self.problem.show(window)
        self.problem.world.show(window)
        for point_i in self.points:
            pg.draw.circle(window,(0,0,128), point_i, 5)

def editor_loop(in_path,bounds=(512,512)):
    obs=Editor(world.read_json(in_path))
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
    obs.problem.world.save(in_path)
    pg.quit()

if __name__ == "__main__":
    if(len(sys.argv)>1):
        editor_loop(sys.argv[1])
    else:
        editor_loop("test.json")
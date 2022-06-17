import pygame as pg
from enum import Enum 
from scipy.spatial import ConvexHull
import numpy as np
import json

class Problem(object):
    def __init__(self,world,start=None,end=None):
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
            self.check()

    def check(self):
        if(len(self.world)>0):
            line=Line(self.start,self.end)
            self.world.polygons[0].check(line)

class World(object):
    def __init__(self):
        self.polygons=[]

    def __len__(self):
        return len(self.polygons)

    def add_polygon(self,points:list):
        polygon_i=make_polygon(points)
        self.polygons.append(polygon_i)

    def show(self,window):
        for pol_i in self.polygons:
            pol_i.show(window) 

    def save(self,out_path):
        data=[pol_i.vertices for pol_i in self.polygons]
        save_json(data,out_path)
        print("save")

class Line(object):
    def __init__(self,a,b):
        self.a=a
        self.b=b

    def is_left(self,c):
        cross=(self.b[0] - self.a[0])*(c[1] - self.a[1]) 
        cross-=(self.b[1] - self.a[1])*(c[0] - self.a[0])
        return cross>0

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def centroid(self):
        return np.mean(self.vertices,axis=0)

    def rotate(self,theta):
        center=self.centroid()
        R=np.array([[np.cos(theta),-np.sin(theta)],
                    [np.sin(theta),np.cos(theta)]])
        self.vertices=[R.dot(vert_i-center)+center
                         for vert_i in self.vertices]

    def check(self,line):
        count=0
        for vert_i in self.vertices:
            if(line.is_left(vert_i)):
                count+=1
        print(count)
    
    def show(self,window):
        pg.draw.polygon(window,(0,128,0),self.vertices)

class EditorMode(Enum):
    OBSTACLE = 1
    START = 2
    END = 3

class Editor(object):
    def __init__(self):
        self.problem=Problem(World())
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

def save_json(data,out_path):
    def helper(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    with open(out_path, 'w') as f:
        json.dump(data, f,default=helper)

def make_polygon(points):
    hull_i=ConvexHull(points)
    hull_points=hull_i.points[hull_i.vertices]
    return Polygon(hull_points)

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
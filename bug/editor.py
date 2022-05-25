import pygame as pg
from scipy.spatial import ConvexHull
import numpy as np
import json

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def show(self,window):
        pg.draw.polygon(window,(0,128,0),self.vertices)

class Obstacles(object):
    def __init__(self):
        self.polygons=[]
        self.points=[]

    def on_click(self,point):
        self.points.append(point)
        print(len(self.points))	

    def on_key(self,key):
        if(len(self.points)>2):
            polygon_i=make_polygon(self.points)
            self.polygons.append(polygon_i)
            self.points.clear()
        print(len(self.polygons))

    def show(self,window):
        window.fill((0,0,0))
        for point_i in self.points:
            pg.draw.circle(window,(0,0,128), point_i, 5)
        for pol_i in self.polygons:
            pol_i.show(window)    

    def save(self,out_path):
        data=[pol_i.vertices for pol_i in self.polygons]
        save_json(data,out_path)
        print("save")

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
    obs=Obstacles()
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
    obs.save("test.json")
    pg.quit()

editor_loop()
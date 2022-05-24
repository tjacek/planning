import pygame as pg
from scipy.spatial import ConvexHull

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def show(self,window):
        print(self.vertices)
        x=30
#        pg.draw.polygon(window, pg.Color('brown'), [(x, 80), (x + 10, 70), (x + 20, 80), (x + 20, 270), (x, 270)])
        pg.draw.polygon(window,(0,128,0),self.vertices)

class Obstacles(object):
    def __init__(self):
        self.polygons=[]
        self.points=[]

    def on_click(self,point):
        print(point)
        self.points.append(point)
        print(len(self.points))	

    def on_key(self,key):
        self.polygons.append(make_polygon(self.points))
        self.points.clear()
        print(len(self.polygons))

    def show(self,window):
        for point_i in self.points:
            pg.draw.circle(window,(0,0,128), point_i, 5)
        for pol_i in self.polygons:
            pol_i.show(window)    

def make_polygon(points):
    hull_i=ConvexHull(points)
    print(dir(hull_i))
    return Polygon(hull_i.points)

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
    pg.quit()

editor_loop()
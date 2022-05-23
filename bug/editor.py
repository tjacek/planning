import pygame as pg

class Obstacles(object):
    def __init__(self):
        self.polygons=[]
        self.points=[]

    def on_click(self,point):
        print(type(point))
        self.points.append(point)
        print(len(self.points))	

def editor_loop(bounds=(512,512)):
    obs=Obstacles()
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
editor_loop()
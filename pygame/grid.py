import numpy as np
import pygame as pg

class Grid(object):
    def __init__(self,x=16,y=16,step=40):
        self.x=x
        self.y=y
        self.step=step
        self.cells=self.make_cells()

    def make_cells(self):
        return [[ pg.Rect((i*self.step)+i,(j*self.step)+j,
                        self.step,self.step)
                    for i in range(self.x)]
                        for j in range(self.y)]

    def show(self,window,color=(255,0,255)):
        for rect_i in self.cells:
            for rect_j in rect_i:	
                pg.draw.rect(window, color, rect_j)

pg.init()
window = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
grid=Grid()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    grid.show(window)
    pg.display.flip()
    clock.tick(3)

pg.quit()
exit()

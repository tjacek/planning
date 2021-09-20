import numpy as np
import pygame as pg

class Grid(object):
    def __init__(self,x=16,y=16,step=40):
        self.x=x
        self.y=y
        self.step=step
        self.cells=empty_cells(x,y,step)

    def get_bounds(self):
        max_x=self.x*self.step+self.x 
        max_y=self.y*self.step+self.y 
        return max_x,max_y

    def get_cord(self,point):
        i= int(point[0]/self.step)
        j= int(point[1]/self.step)
        return i,j 

    def colide(self,point):
        bounds=self.get_bounds() 
        return point[0]<bounds[0] and point[1]<bounds[1]

    def show(self,window,color=(255,0,255)):
        for cell_i in self.cells:
            for cell_j in cell_i:
                cell_j.show(window)

class Cell(object):
    def __init__(self,rect,active=False):
        self.rect=rect
        self.active=active

    def get_color(self):
        return (255,0,0) if(self.active) else (0,255,0)

    def show(self,window):
        color=self.get_color()	
        pg.draw.rect(window, color, self.rect)

def empty_cells(x,y,step):
    return [[ make_cell((i*step)+i,(j*step)+j,step)
                for i in range(x)]
                    for j in range(y)]

def make_cell(x,y,step,active=False):
    rect=pg.Rect(x,y,step,step)
    return Cell(rect,active=active)

pg.init()
window = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
grid=Grid()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONUP:
            point = pg.mouse.get_pos()
            if( grid.colide(point)):
            	i,j=grid.get_cord(point)
            	grid.cells[j][i].active=True
            	print((i,j))
    grid.show(window)
    pg.display.flip()
    clock.tick(3)

pg.quit()
exit()

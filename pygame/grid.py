import numpy as np
import pygame as pg
import os.path

class Grid(object):
    def __init__(self,cells,x=16,y=16,step=40):
        self.x=x
        self.y=y
        self.step=step
        self.cells=cells

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

    def save(self,out_path):
        txt=str(self)
        out_file = open(out_path,"w")
        out_file.write(txt)
        out_file.close()

    def __str__(self):
        s=[ "".join([str(cell_j) for cell_j in cell_i])
                for cell_i in self.cells]
        return "\n".join(s)

class Cell(object):
    def __init__(self,rect,active=False):
        self.rect=rect
        self.active=active

    def get_color(self):
        return (255,0,0) if(self.active) else (0,255,0)

    def flip(self):
        self.active=not self.active

    def show(self,window):
        color=self.get_color()	
        pg.draw.rect(window, color, self.rect)

    def __str__(self):
        return str(int(self.active))

def empty_grid(x=16,y=16,step=40):
    cells=[[ make_cell(i,j,step)
                for i in range(x)]
                    for j in range(y)]
    return Grid(cells,x,y,step)

def make_cell(i,j,step,active=False):
    x,y=i*step+i,j*step+j
    rect=pg.Rect(x,y,step,step)
    return Cell(rect,active=active)

def read_grid(in_path,step=40):
    in_file = open(in_path, "r")
    txt=in_file.read()
    cells=[]
    for i,cell_i in enumerate(txt.split("\n")):
        cells.append([])
        for j,cell_j in enumerate( cell_i):
            active= bool(int(cell_j))
            cells[-1].append(make_cell(i,j,step,active))
    cells=[list(i) for i in zip(*cells)]
    x,y=len(cells),len(cells[0])
    return Grid(cells,x,y,step)

def grid_exp(out_path):
    if(os.path.isfile(out_path)):
        grid=read_grid(out_path)
    else:
        grid=empty_grid()
    grid_loop(grid)
    grid.save(out_path)
    pg.quit()
    exit()

def grid_loop(grid):
    pg.init()
    window = pg.display.set_mode((1000, 1000))
    clock = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                if( grid.colide(point)):
            	    i,j=grid.get_cord(point)
            	    grid.cells[j][i].flip()
            	    print((i,j))
        grid.show(window)
        pg.display.flip()
        clock.tick(3)

grid_exp("test.txt")
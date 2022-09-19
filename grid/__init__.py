import numpy as np
import pygame as pg
from enum import Enum
import os.path

class Grid(object):
    def __init__(self,cells,x=16,y=16,step=40,color_map=None):
        if(color_map is None):
            color_map=default_color_map
        self.x=x
        self.y=y
        self.step=step
        self.cells=cells
        self.color_map=color_map

    def __getitem__(self,cord):
        return self.cells[cord[0]][cord[1]]

    def get_bounds(self):
        max_x=self.x*self.step+self.x 
        max_y=self.y*self.step+self.y 
        return max_x,max_y
    
    def near(self,i,j):
        candidates=[(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),
                    (i,j-1),(i+1,j-1),(i+1,j),(i+1,j+1)]
        return [cand for cand in candidates
                  if(self.valid(*cand))]

    def valid(self,i,j):
        if(i<0 or j<0):
            return False
        if( i>=self.x or j>=self.y):
            return False
        if(self.cells[i][j].active()):
            return False
        return True
    
    def get_cord(self,point):
        i= int(point[0]/self.step)
        j= int(point[1]/self.step)
        return i,j 

    def colide(self,point):
        bounds=self.get_bounds() 
        return point[0]<bounds[0] and point[1]<bounds[1]

    def show(self,window):
        for cell_i in self.cells:
            for cell_j in cell_i:
                cell_j.show(window)

    def save(self,out_path):
        txt=str(self)
        out_file = open(out_path,"w")
        out_file.write(txt)
        out_file.close()

    def set_color(self,cord,color_id):
        cell=self[cord]
        color=self.color_map(cell,color_id)
        cell.color=color

    def __str__(self):
        s=[ "".join([str(cell_j) for cell_j in cell_i])
                for cell_i in self.cells]
        return "\n".join(s)

class CellColors(Enum):
    empty=(0,255,0)
    obst=(255,0,0)
    path=(0,0,255)
    goal=(0,0,128)

class Cell(object):
    def __init__(self,rect,color=CellColors.empty):
        self.rect=rect
        self.color=color

    def active(self):
        return self.color==CellColors.obst

    def show(self,window):
        color=self.color.value
        pg.draw.rect(window, color, self.rect)

    def __str__(self):
        return str(int(self.active()))

class SimpleContoler(object):
    def __init__(self,grid):
        self.grid=grid

    def on_click(self,point):
        if(self.grid.colide(point)):
            cord=self.grid.get_cord(point)
            self.grid.set_color(cord,None)        
            print(cord)

    def on_key(self,key):
        print(key)

def default_color_map(cell,color_id):
    if(type(color_id)==str):
        return CellColors[color_id]
    print(color_id)
    if(cell.color==CellColors.empty):
        return CellColors.obst
    else:
        return CellColors.empty

def empty_grid(x=16,y=16,step=40):
    cells=[[ make_cell(i,j,step)
                for i in range(x)]
                    for j in range(y)]
    return Grid(cells,x,y,step)

def make_cell(i,j,step,color=False):
    if(color):
        color=CellColors.obst
    else:
        color=CellColors.empty
    x,y=i*step+i,j*step+j
    rect=pg.Rect(x,y,step,step)
    return Cell(rect,color)

def read_grid(in_path,step=40):
    in_file = open(in_path, "r")
    txt=in_file.read()
    cells=[]
    for i,cell_i in enumerate(txt.split("\n")):
        cells.append([])
        for j,cell_j in enumerate( cell_i):
            active= bool(int(cell_j))
            cells[-1].append(make_cell(i,j,step,active))
    x,y=len(cells),len(cells[0])
    return Grid(cells,x,y,step)

def from_array(array,step=5):
    x,y=array.shape
    cells=[]
    for i in range(x):
        cells.append([])
        for j in range(y):
            active= (array[i][j]>0)
            cells[-1].append(make_cell(i,j,step,active))
    return Grid(cells,x,y,step)

def grid_exp(out_path):
    if(os.path.isfile(out_path)):
        grid=read_grid(out_path)
    else:
        grid=empty_grid()
    grid_loop(SimpleContoler(grid))
    grid.save(out_path)
    pg.quit()
    exit()

def grid_loop(controler):
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
                controler.on_click(point)
            if event.type == pg.KEYDOWN:
                controler.on_key(event.key)
        controler.grid.show(window)
        pg.display.flip()
        clock.tick(3)

if __name__ == "__main__":
    grid_exp("test.txt")
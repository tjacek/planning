import sys
sys.path.insert(0,'..')
import numpy as np
import pygame as pg
import world,grid

def get_grid(in_path,step=5,margin=10):
    problem=world.read_json(in_path)
    result=problem.world.get_max()
    result+=margin
    dims=(result/step).astype(int)+1
    grid_arr=np.zeros(dims)
    x,y=step/2,step/2
    for i in range(dims[0]):
        for j in range(dims[1]):
            x_i,y_i= x+(i*step),y+(j*step)
            if(problem.world.inside((x_i,y_i))):
            	grid_arr[i][j]=1
    disc=grid.from_array(grid_arr,2*step)
    return disc
#    print(np.sum(grid_arr))

if __name__ == "__main__":
    disc=get_grid('test.json')
    grid.grid_loop(grid.SimpleContoler(disc))
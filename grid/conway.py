import numpy as np
import grid

class ConwayControler(object):
    def __init__(self,grid):
        self.grid=grid

    def on_click(self,point):
        self.next_step()

    def on_key(self,key):
        self.next_step()
    
    def next_step(self):
        x,y=self.grid.x,self.grid.y
        next_state=[[ self.is_alive(i,j)
                        for i in range(x)]
                            for j in range(y)]
        next_state=np.array(next_state)
        for cord, alive in np.ndenumerate(next_state):
            if(alive):
                self.grid.set_color(cord,"obst")
            else: 
                self.grid.set_color(cord,"empty")

    def is_alive(self,i,j):
        n_alive=8-len(self.grid.near(i,j))
        active=self.grid[(i,j)].active()
        if(active and n_alive==3):
            return True
        if(not active and (n_alive==2 or n_alive==3)):
            return True
        return False

def game_of_life(in_path,step=40):
    raw_grid=grid.read_grid(in_path,step)
    controler=ConwayControler(raw_grid)
    grid.grid_loop(controler)

game_of_life("test.txt")
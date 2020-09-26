import numpy as np

class Grid(object):
    def __init__(self, grid):
        self.grid = grid

    def __getitem__(self,key):
        return self.grid[key]	

    def valid(self,pair):
        if(pair[0]<0 or pair[1]<0):
            return False
        bound=[ value>=bound  
        	        for value,bound in zip(pair,self.grid.shape)]
        if(any(bound)):
        	return False
        return self.grid[pair[0],pair[1]]==0
	
    def get_grid(self):
        text=self.grid.astype(str)
        text[text=='0']='.'
        text[text=='1']='#'
        return text

def read_grid(in_path):
    with open (in_path, "r") as grid_file:
        text=[[c_j for c_j in line_i] 
                for line_i in grid_file.read().split('\n')]
        text=np.array(text)
        text[text=='#']='1'
        text[text!='1']='0'
        text=text.astype(int)
        return Grid(text)
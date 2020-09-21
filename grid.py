import numpy as np 

def read_grid(in_path):
    with open (in_path, "r") as grid_file:
        text=[[c_j for c_j in line_i] 
                for line_i in grid_file.read().split('\n')]
        text=np.array(text)
        text[text=='#']='1'
        text[text!='1']='0'
        text=text.astype(int)
        return text

read_grid("sample.txt")        
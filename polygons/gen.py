import sys
sys.path.append("..")
import numpy as np
import polygons 

def gen_world(n_rect,bound_world=(800,800),
        bound_width=(5,50),bound_height=(5,20)):
    rects=[]
    for i in range(n_rect):
        x=np.random.uniform(0,bound_world[0])
        y=np.random.uniform(0,bound_world[1])
        width=np.random.uniform(bound_width[0],bound_width[1])
        height=np.random.uniform(bound_width[0],bound_width[1])
        rects.append(make_rect(x,y,width,height))
    return polygons.World(rects)

def make_rect(x,y,width,height):
	vertices=[[x,y],[x+width,y],[x+width,y+height],
	        [x,y+height]]
	return polygons.Polygon(vertices)
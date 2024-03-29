#import sys
#sys.path.append("..")
import numpy as np
import polygons 

def cell_world(n_rect):
    world=gen_world(n_rect)
    world.move(random_rotation(n_rect))
    a_min=world.get_box()[0]
    world.move(polygons.RigidMotion(0,-a_min[0],-a_min[1]))
    return world

def gen_world(n_rect,bound_world=(400,400),
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

def random_rotation(n=None):
    theta=np.random.uniform(0,2*np.pi,size=n)
    if(n is None):
        return polygons.RigidMotion(theta,0.0,0.0)
    else:
        return [polygons.RigidMotion(theta_i,0.0,0.0)
                    for theta_i in theta]
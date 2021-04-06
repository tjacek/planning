import numpy as np
import convex,collision,plot

def rect_world(n_rect,min_size=1,max_size=3,world_x=10,world_y=10):
	squares=[]
	for i in range(n_rect):
		width,height=np.random.uniform(min_size,max_size,2)
		x=np.random.uniform(0.0,world_x)
		y=np.random.uniform(0.0,world_y)
		squares.append(make_rect(x,y,width,height))
	return collision.World2D(squares)

def make_rect(x,y,width,height):
	vertices=[np.array([x,y]),
			  np.array([x+width,y]),
			  np.array([x+width,y+height]),
			  np.array([x,y+height])]
	return convex.ConvexPolygon(vertices)

#make_square(1,2,4,5)
world=rect_world(5)
plot.plot_polygon(world.obstacles)
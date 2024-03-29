import sys
sys.path.append("..")
import numpy as np
import convex,collision,plot,world2D,states

def make_problem(n_rect=5,width=1,height=5,gap=1):
	obst=rect_world(n_rect)
	box=obst.get_box()
	x,y=box.min-gap
	x,y=x-width,y-height
	start=make_rect(x,y,width,height)
	start=states.State([0,0,0],start)
	x_e,y_e=box.max+gap
#	x_e,y_e=x+width,y+height
	end=make_rect(x_e,y_e,width,height)
	end=states.State([0,x_e-x,y_e-y] ,end)
	return world2D.Problem(start,end,obst)

def rect_world(n_rect,min_size=1,max_size=3,world_x=10,world_y=10):
	squares=[]
	for i in range(n_rect):
		width,height=np.random.uniform(min_size,max_size,2)
		x=np.random.uniform(0.0,world_x)
		y=np.random.uniform(0.0,world_y)
		squares.append(make_rect(x,y,width,height))
	return collision.PolygonEnvir(squares)

def make_rect(x,y,width,height):
	vertices=[np.array([x,y]),
			  np.array([x+width,y]),
			  np.array([x+width,y+height]),
			  np.array([x,y+height])]
	return convex.ConvexPolygon(vertices)

def check_boxes(envir):
    boxes=envir.boxes
    for box_i in boxes:
        for box_j in boxes:
            if(box_i!=box_j):
                plot.plot_box([box_i,box_j])
                box_coll=(box_i,box_j,box_i(box_j),box_j(box_i))
                print("%s;%s;%d,%d" % box_coll)

if __name__ == "__main__":
    problem=make_problem(n_rect=5)
    #problem.save("square.json")
    #problem=world2D.read_problem("square.json")
    import grid
    positions=grid.grid_search(problem,(10,10,10))  #problem.legal(5)[0]
    #plot.plot_positions(positions)
    plot.plot_problem(problem,positions,False)
    #plot.plot_problem(problem,positions,True)
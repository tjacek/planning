import numpy as np

class Halton(object):
    def __init__(self,p=(2,3,5)):
        self.p=p

    def __call__(self,n):
        return [corput(n,p_j) for p_j in self.p]

def corput(n,base):
    q,bk=0,1/base
    while(n>0):
        q+=(n %base)*bk
        n/=base
        bk/=base
    return q

def sample_quasi(problem,n):
    min_point,width,height=problem.get_bounds()
    scale=[2*np.pi,width,height]
    quasi_seq=Halton((2,3,5))
    polygons=[]
    for i in range(n):
        raw_i=np.array(quasi_seq(i+1))
        point_i= scale*raw_i
        point_i[1]+=min_point[0]
        point_i[2]+=min_point[1]
        polygon_i=problem.legal_position(point_i)
        if(polygon_i):
            polygons.append(polygon_i)	
    return polygons

import sys
sys.path.append("..")
import world2D,plot
problem=world2D.read_problem("square.json")
polygons=sample_quasi(problem,100)
plot.plot_problem(problem,polygons,False)
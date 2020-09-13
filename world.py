import numpy as np 

class ConvexPolygon(object):
    def __init__(self,half_planes):
        self.half_planes=half_planes

    def __call__(self,point):
        bool_arr=[ half_plane_i(point)
                    for half_plane_i in self.half_planes]	
        return all(bool_arr)

class HalfPlane(object):
    def __init__(self,a,b,c):
        self.coff=np.array([a,b,c])

    def __call__(self,point):
        f=np.sum(self.coff[:-1]*point)
        return (f+self.coff[-1])>0.0

def make_point(x,y):
    return np.array([x,y])

#plane=HalfPlane(0.0,1.0,-1.0)
#print(plane(make_point(1.0,1.0)))
a=[ HalfPlane(1.0,1.0,1.0),HalfPlane(1.0,1.0,-1.0),
    HalfPlane(-1.0,1.0,1.0),HalfPlane(-1.0,1.0,-1.0)]
polygon=ConvexPolygon(a)
print(polygon(make_point(0.0,100.0)))


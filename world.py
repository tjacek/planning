import numpy as np 
import matplotlib.pyplot as plt

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

def plot_polygon(polygon,n=100,scale=100):
    points=scale*np.random.random_sample((n,2))
    points=[ point_i
                for point_i in points
                    if(polygon(point_i))]
    print(len(points))
    plt.figure()
    ax = plt.subplot(111)
    points=np.array(points)
    plt.scatter(points[:,0],points[:,1])
    plt.show()


a=[ HalfPlane(1.0,1.0,1.0),HalfPlane(1.0,1.0,-1.0),
    HalfPlane(-1.0,1.0,1.0),HalfPlane(-1.0,1.0,-1.0)]
polygon=ConvexPolygon(a)
plot_polygon(polygon,n=1000)
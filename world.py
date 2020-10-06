import numpy as np 
import matplotlib.pyplot as plt

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def __len__(self):
        return self.vertices.shape[0]

    def __call__(self,point):
        size=len(self)
        cord=[(i,i+1) for i in range(size-1)]
        cord.append((size-1,0))
        inside=False
        x,y=point[0],point[1]
        for cord_i in cord:
            print(cord_i)
            b_i=self.vertices[cord_i[0]]
            e_i=self.vertices[cord_i[1]]
            cross_i=(b_i[0]<=x and e_i[0]>=x) or (e_i[0]<=x and b_i[0]>=x)
#x < ((xj - xi) * (y - yi) / (yj - yi) + xi)
            left_i= x<((e_i[0]-b_i[0])*(y-b_i[1])/(e_i[1]-b_i[1]) +b_i[0])
            if(cord_i and left_i):
                inside=not inside
        return inside

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

#vertices=np.array([[-1,1],[0,0],[1,1],[1,-1],[-1,-1]])

vertices=np.array([[-1,1],[1,1],[1,-1],[-1,-1]])
polygon=Polygon(vertices)
print(polygon(np.array([100.0,-0.5])))
#a=[ HalfPlane(1.0,1.0,1.0),HalfPlane(1.0,1.0,-1.0),
#    HalfPlane(-1.0,1.0,1.0),HalfPlane(-1.0,1.0,-1.0)]
#polygon=ConvexPolygon(a)
#plot_polygon(polygon,n=1000)
import numpy as np

class ConvexPolygon(object):
    def __init__(self,vertices):
        if(vertices.shape[1]!=2):
            raise Exception("Wrong number of dims %d" % vertices.shape[1])
        self.vertices=vertices

    def __len__(self):
        return len(self.vertices)

    def __call__(self,point):
        cord=[ (i,i+1) for i in range(len(self)-1)] 
        cord.append((len(self)-1,-1))
        for x,y in cord:
            if(is_left(self.vertices[x],self.vertices[y],point)):
                return False
        return True

    def move(self,motion):
        new_points=[motion(vert_i) for vert_i in self.vertices]
#        raise Exception(new_points[0].shape)
        return ConvexPolygon(np.array(new_points))

def is_left(a,b,c):
    return ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>0
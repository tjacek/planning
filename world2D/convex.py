import numpy as np

class ConvexPolygon(object):
    def __init__(self,vertices):
        if(type(vertices)==list):
            vertices=np.array(vertices) 
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
        return ConvexPolygon(np.array(new_points))

    def get_box(self):
        v_min=np.amin(self.vertices,axis=0)
        v_max=np.amax(self.vertices,axis=0)
        return Box(v_min,v_max)

class Box(object):
    def __init__(self,v_min,v_max):
        self.v_min=v_min
        self.v_max=v_max

    def __add__(self,box_i):
        min_i=np.amin([self.v_min,box_i.v_min],axis=0)
        max_i=np.amax([self.v_max,box_i.v_max],axis=0)
#        raise Exception(min_i.shape)
        return Box(min_i,max_i)

def is_left(a,b,c):
    return ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>0
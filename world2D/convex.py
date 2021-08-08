import numpy as np

class ConvexPolygon(object):
    def __init__(self,vertices):
        if(type(vertices)==list):
            vertices=np.array(vertices) 
        if(vertices.shape[1]!=2 or vertices.ndim!=2):
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
    def __init__(self,box_min,box_max):
        if(type(box_min)==list):
            box_min=np.array(box_min)
        if(type(box_max)==list):
            box_max=np.array(box_max)
        self.min=box_min
        self.max=box_max

    def __call__(self,box):
        a= all(self.min<box.max)
        b= all(box.min< self.max)
        return a and b
        
    def __add__(self,box_i):
        min_i=np.amin([self.min,box_i.min],axis=0)
        max_i=np.amax([self.max,box_i.max],axis=0)

        return Box(min_i,max_i)

    def __str__(self):
        bounds=(self.min[0],self.max[0],self.min[1],self.max[1])
        return "[%.4f-%.4f,%.4f-%.4f]" % bounds

def is_left(a,b,c):
    return ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>0

def get_box(polygons):
    boxes=[pol_i.get_box() for pol_i in polygons]
    box=boxes[0]
    for box_i in boxes[1:]:
        box+=box_i
    return box

if __name__ == "__main__":
    a=Box([-2,-2],[3,3])
    b=Box([0,0],[2,2])
    print(a(b) )

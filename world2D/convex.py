import numpy as np

class ConvexPolygon(object):
    def __init__(self,vertices):
        if(type(vertices)==list):
            vertices=np.array(vertices) 
        if(vertices.shape[1]!=2 or vertices.ndim!=2):
            raise Exception("Wrong number of dims %d" % vertices.shape[1])
        self.vertices=vertices
        self.centroid=None

    def __len__(self):
        return len(self.vertices)

    def __call__(self,point):
        previous_side=None
        n_vertices = len(self)
        for n in range(n_vertices):
            a,b=self.vertices[n],self.vertices[(n+1)%n_vertices]
            affine_segment = v_sub(b,a)
            affine_point = v_sub(point,a)
            current_side = get_side(affine_segment, affine_point)
            if current_side is None:
                return False 
            elif previous_side is None:
                previous_side = current_side
            elif previous_side != current_side:
                return False
        return True

    def get_centroid(self):
        if(self.centroid is None):
            self.centroid= np.mean(self.vertices,axis=0)
        return self.centroid
        
    def as_edges(self):
        n_vert = len(self)
        return [ v_sub(self.vertices[i],self.vertices[(i+1)%n_vert])
                    for i in range(n_vert)]

    def move(self,motion):
        center=self.get_centroid()
        new_points=[motion(vert_i-center)+center for vert_i in self.vertices]
        return ConvexPolygon(np.array(new_points))

    def get_box(self):
        v_min=np.amin(self.vertices,axis=0)
        v_max=np.amax(self.vertices,axis=0)
        return Box(v_min,v_max)

    def __str__(self):
        return str(self.vertices)

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

    def as_point(self):
        height= self.max[1]-self.min[1]
        width= self.max[0]-self.min[0]
        return self.min,width,height

    def __str__(self):
        bounds=(self.min[0],self.max[0],self.min[1],self.max[1])
        return "[%.4f-%.4f,%.4f-%.4f]" % bounds

def get_box(polygons):
    boxes=[pol_i.get_box() for pol_i in polygons]
    min_all=np.amin([ box_i.min for box_i in boxes],axis=0)
    max_all=np.amax([ box_i.max for box_i in boxes],axis=0)
    return Box(min_all,max_all)

def v_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def get_side(a, b):
    x = cosine_sign(a, b)
    if x < 0:
        return 0
    elif x > 0: 
        return 1
    else:
        return None

def cosine_sign(a, b):
    return a[0]*b[1]-a[1]*b[0]

if __name__ == "__main__":
    a=ConvexPolygon([[-2,-2],[2,-2],[2,2],[-2,2]])
#    a=ConvexPolygon([[0,-1],[-1,0],[0,1],[1,0]])
    print(a.as_edges())
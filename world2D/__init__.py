import numpy as np

class World2D(object):
    def __init__(self, obstacles,robot):
        self.obstacles=obstacles
        self.robot = robot

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def __len__(self):
        return self.vertices.shape[0]

    def __getitem__(self, key):
        return self.vertices[key]

    def get_segments(self):
        segments=[ [self.vertices[i],self.vertices[i+1]] 
                    for i in range(len(self)-1)]
        segments.append([self.vertices[-1],self.vertices[0]])
        return segments

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
            left_i= x<((e_i[0]-b_i[0])*(y-b_i[1])/(e_i[1]-b_i[1]) +b_i[0])
            if(cord_i and left_i):
                inside=not inside
        return inside

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b

def seq_intersection(seg_i,seg_j):
    A,B=seg_i 
    C,D=seg_j
    p,q,r=A-C,B-A,D-C
    if(q[0]*r[1] - q[1]*r[0]):
        t = (q[1]*p[0] - q[0]*p[1])/(q[0]*r[1] - q[1]*r[0]) 
    else:
        t=(q[1]*p[0] - q[0]*p[1])
    if(q[0]!=0):
        u = (p[0] + t*r[0])/q[0]
    else:
        u=(p[1] + t*r[1])/q[1]
    return t>0 and t<=1 and u>=0 and u<=1
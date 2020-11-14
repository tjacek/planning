import numpy as np
import re 
import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

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

def plot_polygon(polygons):#,n=100,scale=100):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    fig, ax = plt.subplots()
    ax.set_xlim([0.0,5.0])
    ax.set_ylim([0.0,5.0])
    ax.add_collection(p)
    plt.show()

def read_polygons(in_path):
    lines=open(in_path,'r').readlines()
    bracket=re.compile("\\[(.*?)\\]")
    polygons=[]
    for line_i in lines:
        line_i=line_i.strip()
        line_i=re.findall(bracket,line_i)
        vertices=[[float(cord_k) 
                    for cord_k in tuple_j.split(",")]
                        for tuple_j in line_i]
        polygons.append(Polygon(np.array(vertices)))
    return polygons

def is_simple(polygon):
    segments=polygon.get_segments()
    for i,seg_i in enumerate(segments):
        for seg_j in segments[i+1:]:
            if(seq_intersection(seg_i,seg_j)):
                return False
    return True

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
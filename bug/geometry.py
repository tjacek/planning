import numpy as np
import pygame as pg
from scipy.spatial import ConvexHull

class ConvexPolygon(object):
    def __init__(self,vertices):
        if(type(vertices)==list):
            vertices=np.array(vertices)
        self.vertices=vertices
        self.centroid=None
        self.radius=None

    def __len__(self):
        return len(self.vertices)

    def show(self,window):
        pg.draw.polygon(window,(0,128,0),self.vertices)

    def get_centroid(self):
        if(self.centroid is None):
            self.centroid=np.mean(self.vertices,axis=0)
        return self.centroid

    def get_radius(self):
        if(self.radius is None):
            center=self.get_centroid()
            self.radius=np.amax([np.linalg.norm(center-vert_i)
                for vert_i in self.vertices])
        return self.radius
    
    def vertex_index(self,vert_k):
        for i,vert_i in enumerate(self.vertices):
            if(all([ x==y for x,y in zip(vert_i,vert_k)] )):
                return i 
        return None

    def get_segments(self):
        segments=[[self.vertices[i],self.vertices[i+1]] 
                    for i in range(len(self)-1)]
        segments.append([self.vertices[-1],self.vertices[0]])
        return segments

    def inside(self,point):
        segments=self.get_segments()
        side=is_left(segments[0],point)
        for segm_i in segments[1:]:
            side_i=is_left(segm_i,point)
            if(side_i!=side):
                return False
            side=side_i
        return True

    def rotate(self,theta):
        center=self.get_centroid()
        R=np.array([[np.cos(theta),-np.sin(theta)],
                    [np.sin(theta),np.cos(theta)]])
        self.vertices=[R.dot(vert_i-center)+center
                         for vert_i in self.vertices]
        self.centroid=None
        self.radious=None

    def from_vertex(self,i):
        if(type(i)!=int):
            i=self.vertex_index(i)
        segms=self.get_segments()
        start,end=segms[:i],segms[i:]
        return end+start

    def vertex_colision(self,vert_i,goal):
        line=(vert_i,goal)
        i=self.vertex_index(vert_i)
        segms=self.from_vertex(i)
        path,collision=[],False
        for i,segm_i in enumerate(segms):
            point=intersection(line,segm_i)
            if(not (point is None)):
                collision=True
                break
            path.append(segm_i)
        if(collision):
            result=path
        else:
            result=[line]
        return result

    def detect_collision(self,line,tabu=None):
        for i,(x,y) in enumerate(self.get_segments()):
            if(tabu and i in tabu):
                continue
            if(is_left(line,x) !=  is_left(line,y)):
               return True
        return False

    def get_intersections(self,line):
        inter_points,segm=[],[]
        for i,segm_i in enumerate(self.get_segments()):
            point=intersection(line,segm_i)
            if(not ( point is None)):
                inter_points.append(point)
                segm.append(segm_i)
        return inter_points,segm

def make_polygon(points):
    hull_i=ConvexHull(points)
    hull_points=hull_i.points[hull_i.vertices]
    return ConvexPolygon(hull_points)

def order_polygons(polygons,point):
    distance=[ np.linalg.norm(pol_i.get_centroid()-point)
                for pol_i in polygons]
    return [polygons[i] for i in np.argsort(distance)]

def is_left(line,c):
    a,b=line
    cross=(b[0] - a[0])*(c[1] - a[1]) 
    cross-=(b[1] - a[1])*(c[0] - a[0])
    return cross>0

def all_intersections(line,segments):
    return [intersection(line,segm_i)
        for segm_i in segments]

def intersection(A,B):
    p,q=np.array(A[0]),np.array(B[0])
    r=np.array(A[1])-p
    s=np.array(B[1])-q
    cross_rs=cross(r,s)
    if( cross_rs==0):
        return None
    t=cross(q-p,s)/cross_rs
    u=cross(q-p,r)/cross_rs
    if(0<t and t<1 and 0<u and u<1):
        return p+t*r#,q+u*s)
    return None

def cross(A, B):
    return A[0] * B[1] - A[1] * B[0]

def dist_to_line(line,point):
    x0,y0=point
    x1,y1=line[0]
    x2,y2=line[1]
    dist= np.abs((x2-x1)*(y1-y0) -(x1-x0)*(y2-y1))
    dist/=np.sqrt( (x2-x1)**2 + (y2-y1)**2)
    return dist

def dist_to_pol(pol,line):
    return dist_to_line(line,pol.get_centroid())

def nearest(objects,point):
    objects=np.array(objects)
    distance= [np.linalg.norm(obj_i-point)
                for obj_i in objects]
    return np.argmin(distance)
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

    def colision(self,line):
        col_segments=[]#,[]
        for i,segm_i in enumerate(self.get_segments()):
            if(is_left(line,segm_i[0]) !=  is_left(line,segm_i[1])):
                col_segments.append(segm_i)
#                indexes.append(i)
        return col_segments#,indexes
    
#    def between(self,indexes):
#        start,end=np.amin(indexes),np.amax(indexes)
#        segments= self.get_segments()
#        return [segments[i] for i in range(start,end)]

    def show(self,window):
        pg.draw.polygon(window,(0,128,0),self.vertices)

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
    xdiff = (A[0][0] - A[1][0], B[0][0] - B[1][0])
    ydiff = (A[0][1] - A[1][1], B[0][1] - B[1][1])
    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')
    d = (det(*A), det(*B))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def det(A, B):
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

def make_polygon(points):
    hull_i=ConvexHull(points)
    hull_points=hull_i.points[hull_i.vertices]
    return ConvexPolygon(hull_points)
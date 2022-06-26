import numpy as np
import pygame as pg
from scipy.spatial import ConvexHull
import json

class World(object):
    def __init__(self):
        self.polygons=[]

    def __len__(self):
        return len(self.polygons)

    def add_polygon(self,points:list):
        polygon_i=make_polygon(points)
        self.polygons.append(polygon_i)

    def show(self,window):
        for pol_i in self.polygons:
            pol_i.show(window) 

    def save(self,out_path):
        data=[pol_i.vertices for pol_i in self.polygons]
        save_json(data,out_path)
        print("save")

class Polygon(object):
    def __init__(self,vertices):
        self.vertices=vertices

    def __len__(self):
        return len(self.vertices)

    def centroid(self):
        return np.mean(self.vertices,axis=0)

    def rotate(self,theta):
        center=self.centroid()
        R=np.array([[np.cos(theta),-np.sin(theta)],
                    [np.sin(theta),np.cos(theta)]])
        self.vertices=[R.dot(vert_i-center)+center
                         for vert_i in self.vertices]

    def get_segments(self):
        segments=[[self.vertices[i],self.vertices[i+1]] 
                    for i in range(len(self)-1)]
        segments.append([self.vertices[-1],self.vertices[0]])
        return segments

    def colision(self,line):
        indexes,col_segments=[],[]
        for i,segm_i in enumerate(self.get_segments()):
            if(is_left(line,segm_i[0]) !=  is_left(line,segm_i[1])):
                col_segments.append(segm_i)
                indexes.append(i)
        return col_segments,indexes
    
    def between(self,indexes):
        start,end=np.amin(indexes),np.amax(indexes)
        segments= self.get_segments()
        return [segments[i] for i in range(start,end)]

    def show(self,window):
        pg.draw.polygon(window,(0,128,0),self.vertices)

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

def save_json(data,out_path):
    def helper(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    with open(out_path, 'w') as f:
        json.dump(data, f,default=helper)

def make_polygon(points):
    hull_i=ConvexHull(points)
    hull_points=hull_i.points[hull_i.vertices]
    return Polygon(hull_points)
import pygame as pg
import numpy as np
import json

class World(object):
    def __init__(self,polygons):
        self.polygons=polygons

    def vertices(self):
        vert=[pol_i.vertices for pol_i in self.polygons]
        return np.concatenate(vert,axis=0).T

    def move(self,motion):
        if(type(motion)==list):
            for motion_i,pol_i in zip(motion,self.polygons):
                pol_i.move(motion_i)
        else:
            for pol_i in self.polygons:
                pol_i.move(motion)

    def show(self,window):
        for pol_i in self.polygons:
            pol_i.show(window)	

    def get_box(self):
        raw=[pol_i.get_box() 
                for pol_i in self.polygons]
        raw=list(zip(*raw))
        p_min=np.amin(raw[0],axis=0)
        p_max=np.amax(raw[1],axis=0)
        return (p_min,p_max)

    def save(self,out_path):
        data=[pol_i.vertices for pol_i in self.polygons]
        save_json(data,out_path)
        print("save")

class Polygon(object):
    def __init__(self,vertices):
        if(type(vertices)==list):
            vertices=np.array(vertices)
        self.vertices=vertices
    
    def __len__(self):
        return len(self.vertices)

    def get_edges(self):
        edges=[]
        size=len(self)
        for i in range(1,size):
            edges.append((self.vertices[i-1],self.vertices[i]))
        edges.append((self.vertices[-1],self.vertices[0]))
        return edges

    def move(self,motion):
        self.vertices=np.array([motion(vert_i)
             for vert_i in self.vertices])

    def show(self,window):
        point=[vert_i for vert_i in self.vertices]
        pg.draw.polygon(window,(0,128,0),point)

    def get_box(self):
        v_min=np.amin(self.vertices,axis=0)
        v_max=np.amax(self.vertices,axis=0)
        return [v_min,v_max]

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.theta=theta    
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b

def read_world(in_path):
    data=read_json(in_path)
    return World([ Polygon(data_i) for data_i in data])

def save_json(data,out_path):
    def helper(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    with open(out_path, 'w') as f:
        json.dump(data, f,default=helper)

def read_json(in_path):
    with open(in_path, 'r') as f:
        return json.load(f)
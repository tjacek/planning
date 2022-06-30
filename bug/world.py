import numpy as np
import pygame as pg
import json,os.path
import geometry

class Problem(object):
    def __init__(self,world=None,start=None,end=None):
        if(world is None):
            world=World()
        self.world=world
        self.start=start
        self.end=end

    def posed(self):
        return (self.start and self.end)

    def show(self,window):
        if(self.start):
            pg.draw.circle(window,(0,64,64), self.start, 5)
        if(self.end):
            pg.draw.circle(window,(64,0,64), self.end, 5)
           

class World(object):
    def __init__(self,polygons=None):
        if(polygons is None):
            polygons=[]
        self.polygons=polygons

    def __len__(self):
        return len(self.polygons)

    def add_polygon(self,points:list):
        polygon_i=geometry.make_polygon(points)
        self.polygons.append(polygon_i)
    
    def remove_polygon(self,pol_i):
        self.polygons=[pol_j for pol_j in self.polygons
                         if(pol_i!=pol_j)]

    def inside(self,point):
        for pol_i in self.polygons:
            if(pol_i.inside(point)):
                return pol_i

    def nearest_polygon(self,line):
        polygons=self.collision(line)
        polygons=geometry.order_polygons(polygons,line[0])        
        return polygons[0]

    def collision(self,line):
        candid=[pol_i for pol_i in self.polygons
            if(geometry.dist_to_pol(pol_i,line)<pol_i.get_radius())]
        return [pol_i for pol_i in candid
                    if(pol_i.detect_collision(line))]
#        coll_dict={}
#        for pol_i in candid:
#            coll_i=pol_i.colision(line)
#            if(coll_i):
#                coll_dict[pol_i]=coll_i
#        return coll_dict

    def show(self,window):
        for pol_i in self.polygons:
            pol_i.show(window) 

    def save(self,out_path):
        data=[pol_i.vertices for pol_i in self.polygons]
        save_json(data,out_path)
        print(f"save at {out_path}")

def save_json(data,out_path):
    def helper(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    with open(out_path, 'w') as f:
        json.dump(data, f,default=helper)

def read_json(in_path):
    if(os.path.exists(in_path)):
        f=open(in_path)
        data = json.load(f)
        polygons=[geometry.ConvexPolygon(points_i) 
            for points_i in data]
        f.close()
        return Problem(World(polygons))
    return Problem()
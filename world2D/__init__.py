import numpy as np
import convex,tools,collision,states

class Problem(object):
    def __init__(self,start,end,collision):
        self.start=start
        self.end=end
        self.collision=collision
    
    def get_bounds(self):
        return self.get_box().as_point()

    def get_box(self):
        return convex.get_box(self.all_polygons())

    def all_polygons(self):
        polygons=[self.start.polygon,self.end.polygon]
        polygons+=self.collision.obstacles
        return polygons

    def get_state(self,raw_point):
        conf_i=self.get_conf(raw_point)
        legal=not self.collision(conf_i)
        return states.State(raw_point,conf_i),legal

    def get_conf(self,raw_point):
        motion_i=RigidMotion(*raw_point)
        return self.start.polygon.move(motion_i)
        
    def as_dict(self):
        return {"start":self.start.vertices,
                "end":self.end.vertices,
                "collision":self.collision.as_numpy()}
    
    def save(self,out_path):
    	tools.save_json(self.as_dict(),out_path)

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.theta=theta	
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b

def read_problem(in_path):
    raw=tools.read_json(in_path)
    start=convex.ConvexPolygon(raw["start"])
    end=convex.ConvexPolygon(raw["end"])
    obstacles=[convex.ConvexPolygon(ver_i) 
            for ver_i in raw["collision"]]
    pol_envir=collision.PolygonEnvir(obstacles)
    return Problem(start,end,pol_envir)

def sample_naive(problem,n):
    bounds=problem.get_box()
    x=np.random.uniform(bounds.min[0],bounds.max[0],size=n)
    y=np.random.uniform(bounds.min[1],bounds.max[1],size=n)
    theta=np.random.uniform(0,2*np.pi,size=n)
    points=np.array([theta,x,y]).T
    return problem.legal(points)
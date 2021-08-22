import numpy as np
import convex,tools,collision

class Problem(object):
    def __init__(self,start,end,collision):
        self.start=start
        self.end=end
        self.collision=collision

    def get_box(self):
        box1=self.start.get_box()
        box2=self.end.get_box()
        box3=self.collision.get_box()
        return box1+box2+box3

    def legal_position(self,raw_point):
        motion_i=RigidMotion(*raw_point)
        position_i=self.start.move(motion_i)
        if(not self.collision(position_i)):
            return position_i
        return False

    def legal(self,raw_points):
        positions=[]
        for point_i in raw_points:
            position_i=self.legal_position(point_i)
            if(position_i):
                positions.append(position_i)	
        return positions
        
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

def grid_sample(problem,n):
    min_point,width,height=problem.get_box().as_point()
    step_theta,step_x,step_y=2*np.pi/n,width/n,height/n,
    positions,points=[],[]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                point_ijk=(i*step_x,j*step_y,k*step_theta)
                position_ijk=problem.legal_position(point_ijk)
                if(position_ijk):
                    positions.append(position_ijk)
                    points.append(point_ijk)
    print(len(positions))
    return positions,points

def sample_naive(problem,n):
    bounds=problem.get_box()
    x=np.random.uniform(bounds.min[0],bounds.max[0],size=n)
    y=np.random.uniform(bounds.min[1],bounds.max[1],size=n)
    theta=np.random.uniform(0,2*np.pi,size=n)
    points=np.array([theta,x,y]).T
    return problem.legal(points)
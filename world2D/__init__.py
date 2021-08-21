import numpy as np
import convex,tools,collision

class Problem(object):
    def __init__(self,start,end,collision):
        self.start=start
        self.end=end
        self.collision=collision
        self.legal_sample=grid_sample

    def get_box(self):
        box1=self.start.get_box()
        box2=self.end.get_box()
        box3=self.collision.get_box()
        return box1+box2+box3

    def legal(self,n):
        return self.legal_sample(self,n)

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
    step_x,step_y,step_theta=width/n,height/n,2*np.pi/n
    positions,motions=[],[]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                cord=(i*step_x,j*step_y,k*step_theta)
                motion=RigidMotion(*cord)
                position=problem.start.move(motion)
                if(not problem.collision(position)):
                    motions.append(motion)	
                    positions.append(position)
    print(len(positions))
    return positions,motions

def legal_sample(problem,n,iters=100):
    bounds=problem.get_box()
    positions,motions=[],[]
    while(n>0):
        motion_i=sample_naive(bounds,1)
        position_i=problem.start.move(motion_i)
        if(not problem.collision(position_i)):
            motions.append(motion_i)	
            positions.append(position_i)
            n-=1
        iters-=1
        if(iters<0):
            raise Exception(n)
    return positions,motions

def sample_naive(bounds,n):
    x=np.random.uniform(bounds.min[0],bounds.max[0],size=n)
    y=np.random.uniform(bounds.min[1],bounds.max[1],size=n)
    theta=np.random.uniform(0,2*np.pi,size=n)
    if(n==1):
        return RigidMotion(theta[0],x[0],y[0])
    return [ RigidMotion(theta[i],x[i],y[i]) for i in range(n)]

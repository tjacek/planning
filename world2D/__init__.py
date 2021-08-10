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

    def sample(self,n):
        bounds=self.get_box()
        x=np.random.uniform(bounds.min[0],bounds.max[0],size=n)
        y=np.random.uniform(bounds.min[1],bounds.max[1],size=n)
        theta=np.random.uniform(0,2*np.pi,size=n)
        if(n==1):
            return RigidMotion(theta[0],x[0],y[0])
        return [ RigidMotion(theta[i],x[i],y[i]) for i in range(n)]

    def gen_position(self):
        motion_i=self.sample(1)
        return self.start.move(motion_i)

    def positions(self,n,iters=100):
        legal_pos=[]
        while(n>0):
            sample_i=self.gen_position()
            if(not self.collision(sample_i)):
                legal_pos.append(sample_i)
                n-=1
            iters-=1
            if(iters<0):
                raise Exception(n)
            print(n)
        return legal_pos

    def illegal_positions(self,n=10):
        illegal_pos=[]
        for i in range(n):
            sample_i=self.gen_position()
            if(self.collision.box_collision(sample_i)):
                illegal_pos.append(sample_i)
        return illegal_pos	

    def as_dict(self):
        return {"start":self.start.vertices,
                "end":self.end.vertices,
                "collision":self.collision.as_numpy()}

    def save(self,out_path):
    	tools.save_json(self.as_dict(),out_path)

class RigidMotion(object):
    def __init__(self,theta,x,y):
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
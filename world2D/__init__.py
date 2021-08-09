import numpy as np
import json
import convex

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

    def positions(self,n,iters=100):
        legal_pos=[]
        while(n>0):
            motion_i=self.sample(1)
            sample_i=self.start.move(motion_i)
            if(not self.collision(sample_i)):
                legal_pos.append(sample_i)
                n-=1
            iters-=1
            if(iters<0):
                raise Exception(n)
            print(n)
        return legal_pos

    def as_dict(self):
        return {"start":self.start.vertices,
                "end":self.end.vertices,
                "collision":self.collision.as_numpy()}

    def save(self,out_path):
        def helper(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        with open(out_path, 'w') as f:
            json.dump(self.as_dict(), f,default=helper)

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b
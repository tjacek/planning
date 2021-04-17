import numpy as np
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
		return [ RigidMotion(theta[i],x[i],y[i]) for i in range(n)]

	def positions(self,n):
		motions=self.sample(n)
		return [ self.start.move(motion_i)for motion_i in motions]

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b
import numpy as np

class Problem(object):
	def __init__(self,start,end,collision):
		self.start=start
		self.end=end
		self.collision=collision


class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b
import numpy as np

class World2D(object):
    def __init__(self, obstacles,robot):
        self.obstacles=obstacles
        self.robot = robot

class RigidMotion(object):
    def __init__(self,theta,x,y):
        self.a=np.array([[np.cos(theta),-np.sin(theta)],
                        [np.sin(theta),np.cos(theta)]])
        self.b=np.array([x,y])

    def __call__(self,point):
        return self.a.dot(point)+self.b
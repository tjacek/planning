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

def polygon_collision(pol1,pol2):
	for ver_i in pol1.vertices:
		if(pol2(ver_i)):
			return True
	for ver_i in pol2.vertices:
		if(pol1(ver_i)):
			return True
	return False

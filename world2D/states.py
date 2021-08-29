import numpy as np

class State(object):
    def __init__(self,point,polygon):
        self.point=point
        self.polygon=polygon

def polygon_metric(state1,state2):
    ver1,ver2=get_vert(state1),get_vert(state2)
    dist=[ np.linalg.norm(x_i-y_i)
            for x_i,y_i in zip(ver1,ver2)]
    return np.mean(dist)

def get_vert(state_i):
    if(type(state_i)==State):
        return state_i.polygon.vertices
    return state_i.vertices
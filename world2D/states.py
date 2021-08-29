import numpy as np

class State(object):
    def __init__(self,point,polygon):
        self.point=np.array(point)
        self.polygon=polygon

class Path(object):
    def __init__(self,states):
        self.states=states

    def as_polygons(self):
        return [state_i.polygon for state_i in self.states]	

def polygon_metric(state1,state2):
    ver1,ver2=get_vert(state1),get_vert(state2)
    dist=[ np.linalg.norm(x_i-y_i)
            for x_i,y_i in zip(ver1,ver2)]
    return np.mean(dist)

def get_vert(state_i):
    if(type(state_i)==State):
        return state_i.polygon.vertices
    return state_i.vertices

def SO2_metric(state1,state2):
    point1,point2=state1.point,state2.point
#    raise Exception(point1)
    diff=point1[:2]-point2[:2]
    value=np.sqrt(np.sum(diff**2))
    theta_diff=np.abs(point1[2]-point2[2])
    value+=np.amin([theta_diff,2*np.pi-theta_diff])
    return value
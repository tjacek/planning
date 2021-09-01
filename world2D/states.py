import numpy as np

class State(object):
    def __init__(self,point,polygon):
        self.point=np.array(point)
        self.polygon=polygon

class Path(object):
    def __init__(self,states):
        self.states=states

    def __len__(self):
        return len(self.states)

    def as_points(self,scale=1.0):
        points=[]
        for i in range(1,len(self.states)):
            start,end=self.states[i-1],self.states[i]
            points+=interpolation(start,end,scale)
        return points

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
    diff=point1[1:]-point2[1:]
    value=np.sqrt(np.sum(diff**2))
    theta_diff=np.abs(point1[0]-point2[0])
    value+=np.amin([theta_diff,2*np.pi-theta_diff])
    return value

def euclidean(state1,state2):
    a,b=state1.point[1:],state2.point[1:]
    return np.linalg.norm(a-b)

def interpolation(start,end,scale=1.0):
    distance=euclidean(start,end)
    n=int(np.floor(distance/scale))
    if(n==0):
       return [end.point]
    diff= (end.point-start.point)/n
    points=[ start.point + diff*i 
                for i in range(int(n))]
    return points
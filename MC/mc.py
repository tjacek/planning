import numpy as np
import dist

class MonteCarlo(object):
    def __init__(self,P,Q):
        self.P=P
        self.Q=Q

    def __call__(self,n=100):
        x=[self.Q.sample()  for i in range(n)]
        w=[self.P(x_i)/self.Q(x_i) for x_i in x]
        w_norm=sum(w)
        return sum([ w_i*x_i for w_i,x_i in zip(w,x)])/w_norm

class SphereUniforn(object):
    def __init__(self,dim=5,r=1.0):
        self.dim=dim
        self.r=r

    def __call__(self,x):
        if(np.linalg.norm(x)<self.r):
             return 1.0
        else:
        	return 0.0

def sphere_mc(dim=5):
    P=SphereUniforn(dim)
    Q=gauss=dist.GaussMulti(dim)
    return MonteCarlo(P,Q)

mc=sphere_mc(dim=5)
print(mc())
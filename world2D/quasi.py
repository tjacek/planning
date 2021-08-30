import numpy as np
import states

class Halton(object):
    def __init__(self,p=(2,3,5)):
        self.p=p

    def __call__(self,n):
        return [corput(n,p_j) for p_j in self.p]

def corput(n,base):
    q,bk=0,1/float(base)
    while(n>0):
        q+=(n %base)*bk
        n/=base
        bk/=base
    return q

def sample_quasi(problem,n):
    alpha=[]
    for point_i in quasi_gen(problem,n):
        polygon_i=problem.legal_position(point_i)
        if(polygon_i):
            state_i=states.State(point_i,polygon_i)
            alpha.append(state_i)	
    return alpha

def quasi_gen(problem,n):
    min_point,width,height=problem.get_bounds()
    scale=[2*np.pi,width,height]
    quasi_seq=Halton((2,3,5))
    for i in range(n):
        raw_i=np.array(quasi_seq(i+1))
        point_i= scale*raw_i
        point_i[1]+=min_point[0]
        point_i[2]+=min_point[1]
        yield point_i

def plot_seq(problem,n=100):
    import matplotlib.pyplot as plt
    points= [point_i[1:] 
                for point_i in quasi_gen(problem,n)]
    points=np.array(points).T
    plt.scatter(points[0], points[1],alpha=0.5)
    plt.show()

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    import square,plot
    problem= square.make_problem() #world2D.read_problem("square.json")
    plot_seq(problem,n=100)
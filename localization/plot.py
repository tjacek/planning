import numpy as np
import matplotlib.pyplot as plt
import model

class MPLViewer(object):
    def __init__(self,envir,v=5,omega=(np.pi/12),pause_time=0.001):
        self.envir=envir
        self.u=np.array([v,omega])
        self.pause_time=pause_time

    def show(self,sim_time=20):
        history=np.array([self.envir.get_state()[:2]])
        for t in range(sim_time):
            state=self.envir.observe()
            pos=state[:2].T
            pos=np.expand_dims(pos,axis=0)
            history = np.vstack([history,pos])
            plt.plot(history[ :,0], history[ :,0], ".g")
            self.envir.act(self.u)
#            plt.cla()
#            plt.pause(self.pause_time)
            plt.show()

def plot_ellipse(x, y, a, b, theta, color="-r", ax=None, **kwargs):

    t = np.arange(0, 2 * np.pi + 0.1, 0.1)
    px = a*np.cos(t)
    py = b*np.sin(t)
    fx = rot_matrix(theta) @ (np.array([px, py]))
    px = np.array(fx[0, :] + x).flatten()
    py = np.array(fx[1, :] + y).flatten()
    if ax is None:
        plt.plot(px, py, color, **kwargs)
    else:
        ax.plot(px, py, color, **kwargs)

def rot_matrix(theta):
    mat=[[np.cos(theta), -np.sin(theta)],
         [np.sin(theta),  np.cos(theta)]]
    return np.array(mat)

if __name__ == '__main__':
    viewer=MPLViewer(model.MotionEnvir())
    viewer.show()
#    plot_ellipse(1,2,3,4,1.2)

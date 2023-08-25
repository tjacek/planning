import numpy as np
import matplotlib.pyplot as plt
import model

class MPLViewer(object):
    def __init__(self,envir,pause_time=0.001):
        self.envir=envir
        self.pause_time=pause_time

    def show(self):
        state=self.envir.observe()
        print(state)
        plt.cla()
        plt.pause(self.pause_time)
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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import model

class MPLViewer(object):
    def __init__(self,envir,v=1,omega=(np.pi/12),pause_time=0.001):
        self.envir=envir
        self.u=np.array([v,omega])
        self.pause_time=pause_time

    def show(self,sim_time=20):
        true=[self.envir.get_state()[:2]]
        obs=[self.envir.observe()]
        for t in range(sim_time):
            true_state=self.envir.get_state()
            obs_state=self.envir.observe()
            pos=true_state[:2].T
            true.append(pos)
            obs.append(obs_state)
            self.envir.act(self.u)
        fig=plt.figure() 
        fig, ax = plt.subplots()
        def animate(i):
            print(i)
            true_i=true[i]
            plt.plot(true_i[0],true_i[1], ".g")
            obs_i=obs[i]
            plt.plot(obs_i[0],obs_i[1], ".r")
        anim=animation.FuncAnimation(fig,
                                     animate,
                                     interval=1000,
                                     frames=sim_time)
        print(dir(anim))
        plt.show()
#            plt.plot(history[ :,0], history[ :,0], ".g")
#            plt.cla()
#            plt.pause(self.pause_time)
#            plt.show()

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
    motion_model=model.simple_motion_model()
    viewer=MPLViewer(motion_model)#model.MotionEnvir())
    viewer.show(100)
#    plot_ellipse(1,2,3,4,1.2)

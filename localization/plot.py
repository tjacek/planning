import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import model

class MPLViewer(object):
    def __init__(self,exp,v=1,omega=(np.pi/12)):
        self.exp=exp
        self.u=np.array([v,omega])

    def show(self,sim_time=20,interval=1000):
        fig=plt.figure() 
        def animate(i):
            print(i)
            true_i,obs_i,pred_i=self.exp(self.u)
            plt.plot(true_i[0],true_i[1],".g")
            plt.plot(obs_i[0],obs_i[1], ".r")
            plt.plot(pred_i[0],pred_i[1],".b")
            a,b,theta=get_elipse(self.exp.alg.estm_cov)
            plot_ellipse(pred_i[0],pred_i[1],a,b,theta,'.b')
        anim=animation.FuncAnimation(fig,
                                     animate,
                                     interval=interval,
                                     frames=sim_time)
        plt.show()


def get_elipse(cov_matrix,chi2=3.0):
    eig_val, eig_vec = np.linalg.eig(cov_matrix)
    if eig_val[0] >= eig_val[1]:
        big_ind,small_ind = 0,1
    else:
        big_ind,small_ind = 1,0
    a = np.sqrt(chi2 * eig_val[big_ind])
    b = np.sqrt(chi2 * eig_val[small_ind])
    theta = math.atan2(eig_vec[1, big_ind], eig_vec[0, small_ind])
    return a,b,theta

def plot_ellipse(x, y, a, b, theta, color="-r", ax=None, **kwargs):

    t = np.arange(0, 2 * np.pi + 0.1, 0.1)
    px = a*np.cos(t)
    py = b*np.sin(t)
    fx = rot_matrix(theta) @ (np.array([px, py]))
    px = np.array(fx[0, :] + x).flatten()
    py = np.array(fx[1, :] + y).flatten()
#    if ax is None:
    plt.plot(px, py, color, **kwargs)
#    else:
#        ax.plot(px, py, color, **kwargs)

def rot_matrix(theta):
    mat=[[np.cos(theta), -np.sin(theta)],
         [np.sin(theta),  np.cos(theta)]]
    return np.array(mat)

if __name__ == '__main__':
    exp=model.Experiment(envir=model.simple_motion_model(),
                         alg=model.ExtendedKalman())
    viewer=MPLViewer(exp)
    viewer.show(100)

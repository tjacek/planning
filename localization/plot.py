import numpy as np
import matplotlib.pyplot as plt

def plot_ellipse(x, y, a, b, theta, color="-r", ax=None, **kwargs):

    t = np.arange(0, 2 * np.pi + 0.1, 0.1)
    px = a*np.cos(t)#[a * math.cos(it) for it in t]
    py = b*np.sin(t)#[b * math.sin(it) for it in t]
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
    plot_ellipse(1,2,3,4,1.2)
    plt.show()
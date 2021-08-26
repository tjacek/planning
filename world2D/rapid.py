import sys
sys.path.append("..")
import numpy as np
from sklearn.neighbors import KDTree
import world2D,quasi

def make_rapid(problem,k):
    polygons,points=quasi.sample_quasi(problem,k)
    points=np.array(points)
    tree=KDTree(points)
    nearest_dist, nearest_ind = tree.query(points, k=2) 
    print(nearest_ind)


problem=world2D.read_problem("square.json")
make_rapid(problem,100)
import numpy as np

def SO2_metric(point1,point2):
	diff=point1[:2]-point2[:2]
	value=np.sqrt(np.sum(diff**2))
    theta_diff=np.abs(point1[2]-point2[2])
    value+=np.amin([theta_diff,2*np.pi-theta_diff])
    return value

import numpy as np
from numpy.lib.stride_tricks import as_strided

def binary_arr(size=(5,5)):
	return np.random.randint(2,size=size)

print(binary_arr())
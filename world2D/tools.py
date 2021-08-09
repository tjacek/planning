import numpy as np
import json

def save_json(data,out_path):
    def helper(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    with open(out_path, 'w') as f:
        json.dump(data, f,default=helper)

def read_json(in_path):
	with open(in_path, 'r') as f:
		return json.load(f)
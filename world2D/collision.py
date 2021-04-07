import numpy as np

class PolygonEnvir(object):
	def __init__(self, obstacles):
		self.obstacles=obstacles
		self.boxes=[ pol_i.get_box() for pol_i in self.obstacles]

	def get_box(self):
		all_boxes=[polygon_i.get_box() 
				for polygon_i in self.obstacles]
		all_boxes=np.array(all_boxes)
		g_min=np.amin(all_boxes[:,0],axis=0)
		g_max=np.amax(all_boxes[:,1],axis=0)
		return g_min,g_max


def polygon_collision(pol1,pol2):
	for ver_i in pol1.vertices:
		if(pol2(ver_i)):
			return True
	for ver_i in pol2.vertices:
		if(pol1(ver_i)):
			return True
	return False
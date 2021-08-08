import numpy as np
import convex

class PolygonEnvir(object):
    def __init__(self, obstacles):
        self.obstacles=obstacles
        self.boxes=[ pol_i.get_box() for pol_i in self.obstacles]

    def __call__(self,pol_i):
        return True

    def get_box(self):
        all_boxes=[polygon_i.get_box() 
                for polygon_i in self.obstacles]
        all_boxes=np.array(all_boxes)
        g_min=np.amin([box_i.min for box_i in all_boxes],axis=0)
        g_max=np.amax([box_i.max for box_i in all_boxes],axis=0)
        return convex.Box(g_min,g_max)

    def __str__(self):
        return ";".join([str(box_i) for box_i in self.boxes])

def polygon_collision(pol1,pol2):
    for ver_i in pol1.vertices:
        if(pol2(ver_i)):
            return True
    for ver_i in pol2.vertices:
        if(pol1(ver_i)):
            return True
    return False
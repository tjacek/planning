import numpy as np
import convex

class PolygonEnvir(object):
    def __init__(self, obstacles):
        self.obstacles=obstacles
        self.boxes=[ pol_i.get_box() for pol_i in self.obstacles]

    def __call__(self,pol_i):
        box_i=pol_i.get_box()
        n_col=0
        for j,box_j in enumerate(self.boxes):
            if(box_i(box_j)):
                print(box_i)
                n_col+=1
                pol_j=self.obstacles[j]
                if(polygon_collision(pol_i,pol_j)):
                    return True 
        print("n_cols:%d" % n_col)
        return False

    def box_collision(self,pol_i):
        box_i=pol_i.get_box()
        for box_j in self.boxes:
            if(box_i(box_j)):
                return True
        return False

    def get_box(self):
        all_boxes=[polygon_i.get_box() 
                for polygon_i in self.obstacles]
        all_boxes=np.array(all_boxes)
        g_min=np.amin([box_i.min for box_i in all_boxes],axis=0)
        g_max=np.amax([box_i.max for box_i in all_boxes],axis=0)
        return convex.Box(g_min,g_max)

    def __str__(self):
        return ";".join([str(box_i) for box_i in self.boxes])

    def as_numpy(self):
        return [pol_i.vertices for pol_i in self.obstacles]

def polygon_collision(pol1,pol2):
    for ver_i in pol1.vertices:
        if(pol2(ver_i)):
            return True
    for ver_i in pol2.vertices:
        if(pol1(ver_i)):
            return True
    return False
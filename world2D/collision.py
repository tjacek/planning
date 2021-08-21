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
                n_col+=1
                pol_j=self.obstacles[j]
                if(polygon_collision(pol_i,pol_j)):
                    return True 
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
    edges =  pol1.as_edges() + pol2.as_edges()
    axes = [get_normal(edge) for edge in edges]
    for axis_i in axes:
        proj1=project(pol1, axis_i)
        proj2=project(pol1, axis_i)
        overlapping = overlap(proj1, proj2)
        if not overlapping:
            return False
    return True	

def get_normal(vector):
    vector=np.array([vector[1], -vector[0]])
    norm = np.sqrt( np.sum(vector**2))
    return vector / norm

def project(polygon, axis_i):
    dots = [np.dot(vertex, axis_i) for vertex in polygon.vertices]
    return [np.min(dots), np.max(dots)]

def overlap(proj1, proj2):
    return min(proj1) <= max(proj2) and min(proj2) <= max(proj1)

if __name__ == "__main__":
    a=convex.ConvexPolygon([[-2,-1],[2,-1],[2,1],[-2,1]])
    b=convex.ConvexPolygon([[-1,-2],[-1,2],[1,2],[1,-2]])
    print(polygon_collision(a,b))
#    import plot
#    plot.plot_polygon([a,b])
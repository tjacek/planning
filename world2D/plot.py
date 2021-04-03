import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import collision

def plot_polygon(polygons):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    fig, ax = plt.subplots()
    g_min,g_max=collision.get_global_box(polygons)
    ax.set_xlim([g_min[0]-1,g_max[0]+1])
    ax.set_ylim([g_min[1]-1,g_max[1]+1])
    ax.add_collection(p)
    plt.show()
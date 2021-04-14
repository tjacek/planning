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
    g_min,g_max=collision.get_box()
    ax.set_xlim([g_min[0]-1,g_max[0]+1])
    ax.set_ylim([g_min[1]-1,g_max[1]+1])
    ax.add_collection(p)
    plt.show()

def plot_problem(problem):
    polygons=problem.collision.obstacles
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    start=[matplotlib.patches.Polygon(problem.start.vertices)] 
    p_start=PatchCollection(start, cmap=matplotlib.cm.jet, alpha=0.4)
    end=[matplotlib.patches.Polygon(problem.end.vertices)] 
    p_end=PatchCollection(end, cmap=matplotlib.cm.jet, alpha=0.4)
    
    fig, ax = plt.subplots()
    box=problem.get_box()
    ax.set_xlim([box.min[0]-1,box.max[0]+1])
    ax.set_ylim([box.min[1]-1,box.max[1]+1])
    ax.add_collection(p)
    ax.add_collection(p_start)
    ax.add_collection(p_end)
    plt.show()
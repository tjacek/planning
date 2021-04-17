import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import collision,convex

def plot_polygon(polygons):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    fig, ax = plt.subplots()
    
    box=convex.get_box(polygons)
    
    ax.set_xlim([box.min[0]-1,box.max[0]+1])
    ax.set_ylim([box.min[1]-1,box.max[1]+1])
    ax.add_collection(p)
    plt.show()

def plot_problem(problem):
    polygons=problem.collision.obstacles
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, alpha=0.4, match_original=True)
#    cmap=matplotlib.cm.jet
    start=[matplotlib.patches.Polygon(problem.start.vertices,
                facecolor = (0,0,1))] 
    p_start=PatchCollection(start, alpha=0.4,match_original=True)
    end=[matplotlib.patches.Polygon(problem.end.vertices,
                 facecolor = (1,0,0))] 
    p_end=PatchCollection(end, alpha=0.4,match_original=True)
    
    fig, ax = plt.subplots()
    box=problem.get_box()
    ax.set_xlim([box.min[0]-1,box.max[0]+1])
    ax.set_ylim([box.min[1]-1,box.max[1]+1])
    ax.add_collection(p)
    ax.add_collection(p_start)
    ax.add_collection(p_end)
    plt.show()
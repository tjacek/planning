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

def plot_problem(problem, positions=None):
    if(type(positions)==int):
        positions=problem.positions(positions)
    polygons=problem.collision.obstacles
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, alpha=0.4, match_original=True)
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
    if(positions):
        positions=[matplotlib.patches.Polygon(polygon_i.vertices,
                                    facecolor=(0.5,0.5,0)) 
                for polygon_i in positions]
        positions=PatchCollection(positions, alpha=0.4,match_original=True)
        ax.add_collection(positions)
    plt.show()
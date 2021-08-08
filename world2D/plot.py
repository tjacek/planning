import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import collision,convex

def plot_polygon(polygons):
    if(type(polygons)!=list):
        polygons=[polygons]
    p=to_patches(polygons,facecolor=(0,1,0))
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

    p=to_patches(polygons,facecolor=(0,1,0))
    p_start=to_patches(problem.start,facecolor=(0,0,1))
    p_end=to_patches(problem.end,facecolor=(1,0,0))

    fig, ax = plt.subplots()
    box=problem.get_box()
    ax.set_xlim([box.min[0]-1,box.max[0]+1])
    ax.set_ylim([box.min[1]-1,box.max[1]+1])
    ax.add_collection(p)
    ax.add_collection(p_start)
    ax.add_collection(p_end)
    if(positions):
        positions=to_patches(positions,facecolor=(0.5,0.5,0))
        ax.add_collection(positions)
    plt.show()

def plot_box(boxes):
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, aspect='equal')
    min_dim=np.array([box_i.min for box_i in boxes])
    min_dim=np.min(min_dim,axis=0)
    max_dim=np.array([box_i.max for box_i in boxes])
    max_dim=np.max(max_dim,axis=0)    
    ax.set_xlim([min_dim[0]-1,max_dim[0]+1])
    ax.set_ylim([min_dim[1]-1,max_dim[1]+1])
    rects=[matplotlib.patches.Rectangle(*box_i.as_point()) 
            for box_i in boxes]
    p = PatchCollection(rects, cmap=matplotlib.cm.jet, alpha=0.4)
    ax.add_collection(p)
    plt.show()

def to_patches(polygons,facecolor=(0,1,0)):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices,facecolor=facecolor) 
                for polygon_i in polygons] 
    return PatchCollection(patches,alpha=0.4,match_original=True)
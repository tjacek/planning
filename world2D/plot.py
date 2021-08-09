import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import collision,convex

def plot_problem(problem, positions=None,boxes=False):
    if(type(positions)==int):
        positions=problem.positions(positions)
    polygons=problem.collision.obstacles
    fig, ax = plt.subplots()
    pol_dict=[(polygons,(0,1,0)),(problem.start,(0,0,1)),
              (problem.end,(1,0,0)), (positions,(0.5,0.5,0))]
    fun=to_rectangle if(boxes) else to_patches
    for pol_i,color_i in pol_dict:
        if(pol_i):
            p_i=fun(pol_i,facecolor=color_i)
            ax.add_collection(p_i)
    box=problem.get_box()
    set_limit(ax,box.min,box.max)
    plt.show()

def plot_positions(positions):
    fig, ax = plt.subplots()
    ax.add_collection( to_patches( positions))
    ax.add_collection( to_rectangle(positions))
    box=convex.get_box(positions)
    set_limit(ax,box.min,box.max)
    plt.show()

def plot_polygon(polygons):
    if(type(polygons)!=list):
        polygons=[polygons]
    p=to_patches(polygons,facecolor=(0,1,0))
    fig, ax = plt.subplots()
    
    box=convex.get_box(polygons)
    
    set_limit(ax,box.min,box.max)
    ax.add_collection(p)
    plt.show()

def plot_box(boxes):
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, aspect='equal')
    min_dim=np.array([box_i.min for box_i in boxes])
    min_dim=np.min(min_dim,axis=0)
    max_dim=np.array([box_i.max for box_i in boxes])
    max_dim=np.max(max_dim,axis=0)    
    set_limit(ax,min_dim,max_dim)

    p=to_rectangle(boxes,facecolor=(0,1,0))
    ax.add_collection(p)
    plt.show()

def to_patches(polygons,facecolor=(0,1,0)):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices,facecolor=facecolor) 
                for polygon_i in polygons] 
    return PatchCollection(patches,alpha=0.4,match_original=True)

def to_rectangle(boxes,facecolor=(0,1,0)):
    if(type(boxes)!=list):
        boxes=[boxes]
    patches=[]
    for box_i in boxes:
        if(type(box_i)!=convex.Box):
            box_i=box_i.get_box()
            print(box_i)
        rect_i=matplotlib.patches.Rectangle(*box_i.as_point(),facecolor=facecolor)
        patches.append(rect_i)
    return PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)

def set_limit(ax,min_dim,max_dim):
    ax.set_xlim([min_dim[0]-1,max_dim[0]+1])
    ax.set_ylim([min_dim[1]-1,max_dim[1]+1])
import numpy as np
import re 
import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import world2D,world2D.triangulation

def check_polygons(in_path):
    polygons=read_polygons(in_path)
    polygons=[ polygon_i  
                for polygon_i in polygons
                    if( is_simple(polygon_i))]
    triangles=[]
    for polygon_i in polygons:
        triangles+=world2D.triangulation.triangulation(polygon_i)
    polygons=[world2D.Polygon(tri) for tri in triangles]
    plot_polygon(polygons)

def plot_polygon(polygons):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    fig, ax = plt.subplots()
    ax.set_xlim([0.0,5.0])
    ax.set_ylim([0.0,5.0])
    ax.add_collection(p)
    plt.show()

def read_polygons(in_path):
    lines=open(in_path,'r').readlines()
    bracket=re.compile("\\[(.*?)\\]")
    polygons=[]
    for line_i in lines:
        line_i=line_i.strip()
        line_i=re.findall(bracket,line_i)
        vertices=[[float(cord_k) 
                    for cord_k in tuple_j.split(",")]
                        for tuple_j in line_i]
        polygons.append(world2D.Polygon(np.array(vertices)))
    return polygons

def is_simple(polygon):
    segments=polygon.get_segments()
    for i,seg_i in enumerate(segments):
        for seg_j in segments[i+1:]:
            if(world2D.seq_intersection(seg_i,seg_j)):
                return False
    return True
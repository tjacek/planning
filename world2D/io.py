import numpy as np
import re 
import matplotlib.pyplot as plt
import matplotlib.patches
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import world2D,world2D.triangulation
import world2D.convex,world2D.polygon

def check_polygons(in_path):
    polygons=read_polygons(in_path)
    polygons=[ polygon_i  
                for polygon_i in polygons
                    if( is_simple(polygon_i))]
    triangles=[]
    for polygon_i in polygons:
        triangles+=world2D.triangulation.triangulation(polygon_i)
    polygons=[world2D.convex.ConvexPolygon(tri) for tri in triangles]
    plot_polygon(polygons)

def plot_polygon(polygons):
    if(type(polygons)!=list):
        polygons=[polygons]
    patches=[matplotlib.patches.Polygon(polygon_i.vertices) 
                for polygon_i in polygons]
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    fig, ax = plt.subplots()
    g_min,g_max=world2D.get_global_box(polygons)
    ax.set_xlim([g_min[0]-1,g_max[0]+1])
    ax.set_ylim([g_min[1]-1,g_max[1]+1])
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
        polygons.append(world2D.polygon.Polygon(np.array(vertices)))
    return polygons

def is_simple(polygon):
    segments=polygon.get_segments()
    for i,seg_i in enumerate(segments):
        for seg_j in segments[i+1:]:
            if(world2D.polygon.seq_intersection(seg_i,seg_j)):
                return False
    return True

def move_trinagle():
    v=np.array([[0.0,0.0],[0.0,2.0],[1.0,0.0]])
    v=world2D.convex.ConvexPolygon(v)
    raise Exception(v.get_box())
    plot_polygon(v)
    motion=world2D.RigidMotion(2.0,3.0,3.0)
    v2=v.move(motion)
    plot_polygon(v2)
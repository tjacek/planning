import numpy as np
import math,sys
EPSILON = math.sqrt(sys.float_info.epsilon)

def triangulation(polygon):
	ear_vertex=[]
	triangles=[]
	polygon_t=[list(vert_i) for vert_i in polygon.vertices]
	point_count=len(polygon)
	while(len(polygon_t)>3):
		for i in range(point_count):
			tri=get_triangle(polygon_t,i)
			if(is_ear(tri[0],tri[1],tri[2],polygon_t)):
				triangles.append(tri)
				del polygon_t[i]
				print(len(polygon_t))
				break
	triangles.append(polygon_t)
	return triangles

def get_triangle(polygon,i):
    return [polygon[i-1],polygon[i],
                polygon[ (i+1) % len(polygon)]]

def is_ear(x,y,z,polygon):
	ear= is_angle_convex(x,y,z) \
	        and triangle_area(x,y,z)>0\
	        and contains_no_points(x,y,z,polygon) 
	return ear

def contains_no_points(p1, p2, p3, polygon):
    for pn in polygon:
        if (np.all(pn==p1) or np.all(pn==p2) or np.all(pn==p3)):
            continue
        elif is_point_inside(pn, p1, p2, p3):
            return False
    return True

def is_point_inside(p, a, b, c):
    area = triangle_area(a,b,c,)
    area1 = triangle_area(p,b,c)
    area2 = triangle_area(p,a,c)
    area3 = triangle_area(p,a,b)
    areadiff = abs(area - sum([area1,area2,area3])) < EPSILON
    return areadiff

def is_angle_convex(x,y,z):
    return triangle_sum(x,y,z) < 0

def triangle_sum(p1,p2,p3):
    x,y,z=(p3[1]-p2[1]),(p1[1]-p3[1]),(p2[1]-p1[1])
    return p1[0]*x+p2[0]*y + p3[0]*z

def triangle_area(p1, p2, p3):
    x,y,z=(p2[1] - p3[1]), (p3[1] - p1[1]),(p1[1] - p2[1])
    return abs((p1[0]*x + p2[0]*y + p3[0]*z) / 2.0)

#print( triangle_area([1,0],[1,1],[0,1]))    
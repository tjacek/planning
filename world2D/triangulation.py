import numpy as np
import math,sys
EPSILON = math.sqrt(sys.float_info.epsilon)

def triangulation(polygon):
	ear_vertex=[]
	triangles=[]

	point_count=len(polygon)
	for i in range(point_count):
		first=polygon[i-1]
		secund=polygon[i]
		last=polygon[(i+1)%point_count]
		if(is_ear(first,secund,last,polygon)):
			ear_vertex.append(secund)
	print(len(ear_vertex))

def is_ear(x,y,z,polygon):
	ear= is_angle_convex(x,y,z) \
	        and triangle_area(x,y,z)>0\
	        and contains_no_points(x,y,z,polygon) 
	return ear

def contains_no_points(p1, p2, p3, polygon):
    for pn in polygon.vertices:
        if (np.all(pn==p1) or np.all(pn==p2) or np.all(pn==p3)):
            print("OK")
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
def is_angle_convex(x,y,z):
    return triangle_sum(x,y,z) < 0

def triangle_sum(p1,p2,p3):
    x,y,z=(p3[1]-p2[1]),(p1[1]-p3[1]),(p2[1]-p1[1])
    return p1[0]*x+p2[0]*y + p3[0]*z

def triangle_area(p1, p2, p3):
    x,y,z=(p2[1] - p3[1]), (p3[1] - p1[1]),(p1[1] - p2[1])
    return abs((p1[0]*x + p2[0]*y + p3[0]*z) / 2.0)

print( triangle_area([1,0],[1,1],[0,1]))    
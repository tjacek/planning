import numpy as np
import queue

class GridGraph(object):
    def __init__(self,vertices):
        self.vertices=vertices
        self.goal=None

    def __getitem__(self,cord):
        return self.vertices[cantor_paring(cord)]

    def set_goal(self,goal):
        if(type(goal)==tuple):
            goal=self[goal]
        self.goal=goal

    def reset(self):
        for vertex_i in self.vertices.values():
            vertex_i.reset()

class Vertex(object):
    def __init__(self,cord,edges=[]):
        self.cord=cord
        self.edges=edges
        self.visited=False
        self.parent=None
        self.cost=np.inf

    def reset(self):
        self.visited=False
        self.parent=None
        self.cost=np.inf

class DijkstraSearch(GridGraph):
    def find_path(self,start):
        if(type(start)==tuple):
            start=self[start]
        return get_path(start)	

    def set_goal(self,goal):
        GridGraph.set_goal(self,goal)
        self.dijkstra(self.goal)

    def dijkstra(self,end):
        self.reset()
        states=list(self.vertices.values())
        end.cost=0
        while(states):
            states.sort(key=lambda x:x.cost,reverse=True)
            state_i=self[states.pop().cord]
            for near_j in state_i.edges:
            	near_j=self[near_j]
            	if(near_j.cost>(state_i.cost+1)):
                    near_j.cost=state_i.cost+1
                    near_j.parent=state_i


class FowardSearch(GridGraph):
    def __init__(self,vertices,queue_type=None):
        super().__init__(vertices)
        if(queue_type is None):
            queue_type=LIFO
        self.queue_type=queue_type

    def find_path(self,start):
        if(type(start)==tuple):
            start=self[start]
        self.reset()
        Q=self.queue_type()
        start.visited=True
        Q.insert(start)
        while(Q):
            x=Q.get_first()
            if(x.cord==self.goal.cord):
                return get_path(self.goal)
            for edge_i in x.edges:
                x_i=self[edge_i]
                if(not x_i.visited):
                    x_i.parent=x
                    x_i.visited=True
                    Q.insert(x_i)
        return False

class LIFO(object):
    def __init__(self):
        self.q=[]

    def __bool__(self):
        return len(self.q)!=0

    def insert(self,x):
        return self.q.append(x)

    def get_first(self):
        return self.q.pop()

class FIFO(object):
    def __init__(self):
        self.q=queue.Queue()

    def get_first(self):
        return self.q.get()

    def insert(self,value):
        return self.q.put(value)

    def __bool__(self):
        return (not self.q.empty())

def cantor_paring(k):
    return (k[0]+k[1])*(k[0]+k[1]+1)/2 + k[1]

def get_grid_graph(raw_grid):
    vertices={}
    for i in range(raw_grid.x):
        for j in range(raw_grid.y):
            cord=(i,j)
            key_ij=cantor_paring(cord)
            vertex_ij=Vertex(cord,raw_grid.near(*cord))
            vertices[key_ij]=vertex_ij
    return vertices

def get_path(start):
    path=[]
    vertex_i=start
    while(vertex_i):
        path.append(vertex_i)
        vertex_i=vertex_i.parent
    print(len(path))
    return path
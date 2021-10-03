import numpy as np
import graph

class FowardSearch(graph.GridGraph):
    def __init__(self,vertices,queue_type=None):
        super().__init__(vertices)
        if(queue_type is None):
            queue_type=LIFO
        self.queue_type=queue_type

    def find_path(self,start):
        if(type(start)==tuple):
            start=self[start]
        self.reset()
        Q=self.queue_type(self)
        start.visited=True
        Q.insert(start)
        while(Q):
            x=Q.get_first()
            if(x.cord==self.goal.cord):
                return graph.get_path(self.goal)
            for edge_i in x.edges:
                x_i=self[edge_i]
                if(not x_i.visited):
                    x_i.parent=x
                    x_i.visited=True
                    Q.insert(x_i)
        return False

class LIFO(object):
    def __init__(self,grid):
        self.q=[]

    def get_first(self):
        return self.q.pop()

    def insert(self,x):
        return self.q.append(x)

    def __bool__(self):
        return len(self.q)!=0

class FIFO(object):
    def __init__(self,grid):
        self.q=queue.Queue()

    def get_first(self):
        return self.q.get()

    def insert(self,value):
        return self.q.put(value)

    def __bool__(self):
        return (not self.q.empty())

class BestFirst(object):
    def __init__(self,grid):
        self.q=[]
        self.goal=grid.goal

    def get_first(self):
        self.q=sorted(self.q,
            key=lambda a:a.cost,reverse=True)
        return self.q.pop()

    def insert(self,value):
        value.cost=metric(value,self.goal)
        self.q.append(value)
    
    def __bool__(self):
        return len(self.q)!=0

def metric(a,b):
    x=a.cord[0]-b.cord[0]
    y=a.cord[1]-b.cord[1]
    return np.sqrt(float(x**2+y**2))
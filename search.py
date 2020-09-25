import numpy as np
import queue

class State(object):
    def __init__(self,state_id):
        self.id=state_id
        self.visited=False
        self.parent=None
        self.cost=np.inf

class FowardSearch(object):
    def __init__(self,priority_queue=None):
        if(priority_queue is None):
            priority_queue=[]
        self.priority_queue=priority_queue

    def __call__(self,x0):
        Q=self.priority_queue
        Q.append(x0)
        x0.visited=True
        while(Q):
            x_i=Q.pop()
            if(self.is_goal(x_i)):
                return True
            for x_j in self.next_state(x_i):
                if(not x_j.visited):
                    x_j.parent=x_i
                    x_j.visited=True
                    Q.append(x_j)
        return False

    def is_goal(self,state_i):
        raise NotImplemented()

    def next_state(self,state_i):
        raise NotImplemented()

class FIFO(object):
    def __init__(self):
        self.q=queue.Queue()

    def pop(self):
        return self.q.get()

    def append(self,value):
        return self.q.put(value)

    def __bool__(self):
        return (not self.q.empty())

class BestFirst(object):
    def __init__(self,heuristic):
        self.heuristic=heuristic
        self.states=[]
        self.goal=None
        self.comp=lambda x:x.cost
    
    def set_goal(self,goal):
        self.goal=goal

    def pop(self):
        self.states.sort(key=self.comp,reverse=False)
        return self.states.pop()

    def append(self,state_i):
        state_i.cost=self.heuristic(state_i,self.goal)
        self.states.append(state_i)

    def __bool__(self):
        return bool(self.states)
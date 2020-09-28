import numpy as np
import queue

class State(object):
    def __init__(self,state_id):
        self.id=state_id
        self.visited=False
        self.parent=None
        self.cost=np.inf

class FowardSearch(object):
    def __init__(self,problem,priority_queue=None):
        if(priority_queue is None):
            priority_queue=[]
        self.problem=problem
        self.priority_queue=priority_queue

    def __call__(self,x0):
        Q=self.priority_queue
        Q.append(x0)
        x0.visited=True
        while(Q):
            x_i=Q.pop()
            if(self.problem.is_goal(x_i)):
                return True
            for x_j in self.problem.next_state(x_i):
                if(not x_j.visited):
                    x_j.parent=x_i
                    x_j.visited=True
                    Q.append(x_j)
        return False

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
        self.states.sort(key=self.comp,reverse=True)
        return self.states.pop()

    def append(self,state_i):
        state_i.cost=self.heuristic(state_i,self.goal)
        self.states.append(state_i)

    def __bool__(self):
        return bool(self.states)

class Dijkstra(object):
    def __init__(self):
        self.states=[]
        self.last=None
        self.comp=lambda x:x.cost

    def pop(self):
        self.states.sort(key=self.comp,reverse=True)
        self.last=self.states.pop()
        return self.last

    def append(self,state_i):
        if(self.last):
            cost_ij=self.last.cost+1
            if(cost_ij<state_i.cost):
                state_i.cost=cost_ij
        else:
            state_i.cost=0
        self.states.append(state_i)

    def __bool__(self):
        return bool(self.states)

class AStar(Dijkstra):
    def __init__(self, heuristic):
        self.heuristic=heuristic
        super().__init__()

    def set_goal(self,goal):
        def cost_fun(state_i):
            g_i=self.heuristic(state_i,goal)
            return state_i.cost+g_i
        self.comp=cost_fun

class Iterative(object):
    def __init__(self):
        self.current=None#[]
        self.next=[]

    def pop(self):
        if(not self.current):
            self.current=self.next
            self.next=[]
        return self.current.pop()

    def append(self,state_i):
        if(self.current is None):
            self.current=[state_i]
        else:
            self.next.append(state_i)

    def __bool__(self):
        return bool(self.current) or bool(self.next)
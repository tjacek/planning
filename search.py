import queue

class State(object):
    def __init__(self,state_id):
        self.id=state_id
        self.visited=False
        self.parent=None

class FowardSearch(object):
    def __init__(self,priority_queue=list):
        self.priority_queue=priority_queue

    def __call__(self,x0):
        Q=self.priority_queue()
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
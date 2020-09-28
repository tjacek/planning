from foward import State

class BidirectionalSearch(object):
    def __init__(self,problem,priority_queue=None):
        if(priority_queue is None):
            priority_queue=SetQueue()
        self.problem=problem
        self.priority_queue=priority_queue

class SetQueue(object):
    def __init__(self):
        self.active_states=[]
        self.all_states=set()

    def pop(self):
        return self.active_states.pop()	

    def append(self,state_i):
        self.append(state_i)
        self.active_states.update(state_i)	

    def __contains__(self, state_i):
        return self.all_states in state_i  

    def __bool__(self):
        return bool(self.active_states)	
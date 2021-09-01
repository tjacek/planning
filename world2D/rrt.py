import numpy as np
import states,quasi

class RRTree(object):
    def __init__(self,state_i):
        self.nodes=[Node(state_i)]

    def near(self,state_i):
        distance=[ states.polygon_metric(node_j.state,state_i)
                        for node_j in self.nodes]  
        return self.nodes[np.argmin(distance)]
    
    def add_node(self,state_i,parent):
        new_node=Node(state_i)
        new_node.parent=parent
        parent.edges.append(new_node)
        self.nodes.append(new_node)

class Node(object):
    def __init__(self,state):
        self.state=state
        self.parent=None
        self.edges=[]

    def get_path(self):
        if(self.parent is None):
            return [self]
        path=self.parent.get_path()
        path.append(self)
        return path	

def rdt_search(problem,k):
    rd_tree=make_rrt(problem,k)
    end=rd_tree.near(problem.end)
    path=end.get_path()
    return states.Path([vertex_i.state for vertex_i in path])

def make_rrt(problem,k):
    alpha=quasi.quasi_gen(problem,k)
    rd_tree=RRTree(problem.start)
    for alpha_i in alpha:
        state_i,legal_i=problem.get_state(alpha_i)
        q_n=rd_tree.near(state_i)
        edge_i=make_edge(state_i,q_n.state,problem,scale=3.0)
        if( len(edge_i)>1):
            rd_tree.add_node(edge_i[0],q_n)
    return rd_tree

def make_edge(state_i,q_n,problem,scale=3.0):
    raw_points=states.interpolation(state_i,q_n,scale)
    edge_i=[]
    for point_j in raw_points:
        state_j,legal_j=problem.get_state(point_j)
        if(legal_j):
            edge_i.append(state_j)
        else:
            edge_i=[]
    return edge_i
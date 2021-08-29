import sys
sys.path.append("..")
import numpy as np
#from sklearn.neighbors import KDTree
import world2D,quasi,states

class RDTree(object):
    def __init__(self,state_i):
        self.nodes=[Node(state_i)]

    def add_node(self,state_i):
        near_node=self.near(state_i)
        node_i=Node(state_i)
        near_node.add_edges(node_i)
        self.nodes.append(node_i)
        return node_i

    def near(self,state_i):
        distance=[ states.polygon_metric(node_i.state,state_i)
                        for node_i in self.nodes]  
        return self.nodes[np.argmax(distance)]

class Node(object):
    def __init__(self,state):
        self.state=state
        self.parent=None
        self.edges=[]

    def add_edges(self,node_i):
        node_i.parent=self	
        self.edges.append(node_i)

    def get_path(self):
        if(self.parent is None):
            return [self]
        path=self.parent.get_path()
        path.append(self)
        return path	

def rdt_search(problem,k):
    rd_tree=make_rapid(problem,k)
    end=rd_tree.add_node(problem.end)
    path=end.get_path()
    return [vertex_i.state for vertex_i in path]

def make_rapid(problem,k):
    alpha=quasi.sample_quasi(problem,k)
    rd_tree=RDTree(problem.start)
    for alpha_i in alpha:
        rd_tree.add_node(alpha_i)
    return rd_tree

import square,plot
problem=square.make_problem()
path=rdt_search(problem,500)
plot.plot_problem(problem,path,False)
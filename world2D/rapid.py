import sys
sys.path.append("..")
import numpy as np
#from sklearn.neighbors import KDTree
import world2D,quasi,states,plot

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
        distance=[ states.polygon_metric(node_j.state,state_i)
                        for node_j in self.nodes]  
        node_min=self.nodes[np.argmin(distance)]
        if(node_min.edges):
           costs=[edge_i.cost for edge_i in node_min.edges]
           return node_min.edges[np.argmin(costs)]
        return node_min

    def get_states(self):
        return [node_i.state for node_i in self.nodes]
    
    def get_level(self,k):
        level=[]
        for node_i in self.nodes:
            if(node_i.height==k):
                level.append(node_i.state)
        return level

class Node(object):
    def __init__(self,state):
        self.height=0
        self.state=state
        self.parent=None
        self.cost=0
        self.edges=[]

    def add_edges(self,node_i):
        node_i.parent=self	
        node_i.height=self.height+1
        prev=node_i.parent
        self.cost=prev.cost=states.polygon_metric(node_i.state,prev.state)
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
    alpha=quasi.quasi_gen(problem,k)
    rd_tree=RDTree(problem.start)
    for alpha_i in alpha:
        state_i,legal_i=problem.get_state(alpha_i)
        if(not legal_i):
            q_n=rd_tree.near(state_i).state
            q_s=problem.stopping_conf(q_n,state_i)
            if(q_n!=q_s):
                print(q_s)
                rd_tree.add_node(q_s)
        else:
            rd_tree.add_node(state_i)		
    return rd_tree

def show_tree(problem,rd_tree):
    k=0
    level_k=rd_tree.get_level(k)
    while(level_k):
        plot.plot_problem(problem,level_k,False)
        k+=1
        level_k=rd_tree.get_level(k)

def rapid_exp(problem=None,n=100):
    if(problem is None):
        problem=square.make_problem()
    path=rdt_search(problem,n)
    plot.plot_problem(problem,path,False)

import square
#path=make_rapid(problem,200).get_states()
#show_tree(problem,path)
rapid_exp(problem=None,n=100)
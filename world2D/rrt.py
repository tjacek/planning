import numpy as np
import states,quasi

class RRTree(object):
    def __init__(self,state_i,metric=states.polygon_metric,radius=None):
        self.nodes=[Node(state_i)]
        self.metric=metric
        self.radius=radius

    def next_node(self,state_i):
        if(self.radius):
            near_nodes=self.in_radius(state_i,self.radius)
            if(not near_nodes):
                return self.near(state_i)
            cost=[node_j.cost for node_j in near_nodes]
            return near_nodes[np.argmin(cost)]
        else:
            return self.near(state_i)

    def near(self,state_i,nodes=None):
        if(nodes is None):
            nodes=self.nodes
        distance=[ self.metric(node_j.state,state_i)
                        for node_j in nodes]  
        return self.nodes[np.argmin(distance)]
    
    def in_radius(self,state_i,r=1.0):
        return [ node_j
                for node_j in self.nodes
                    if(self.metric(node_j.state,state_i)<r)]


    def add_node(self,state_i,parent):
        new_node=Node(state_i)
        new_node.parent=parent
        parent.edges.append(new_node)
        if(self.radius):
            distance=self.metric(parent.state,state_i)
            new_node.cost=distance + parent.cost
        self.nodes.append(new_node)
        return new_node

class Node(object):
    def __init__(self,state):
        self.state=state
        self.cost=0.0
        self.parent=None
        self.edges=[]

    def get_path(self):
        if(self.parent is None):
            return [self]
        path=self.parent.get_path()
        path.append(self)
        return path	

def rdt_search(problem,k,scale=3.0,radius=3.0):
    rr_tree=make_rrt(problem,k,scale,radius)
    end=make_node(problem.end.point,rr_tree,problem,scale)
    path=end.get_path()
    return states.Path([vertex_i.state for vertex_i in path])

def make_rrt(problem,k,scale,radius=3.0):
    alpha=quasi.quasi_gen(problem,k)
    rr_tree=RRTree(problem.start,radius=radius)
    for alpha_i in alpha:
        make_node(alpha_i,rr_tree,problem,scale)
    return rr_tree

def make_node(alpha_i,rr_tree,problem,scale=3.0):
    state_i,legal_i=problem.get_state(alpha_i)
    q_n=rr_tree.next_node(state_i)
    edge_i=make_edge(state_i,q_n.state,problem,scale)
    if( len(edge_i)>1):
        return rr_tree.add_node(edge_i[0],q_n)    
    return q_n

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
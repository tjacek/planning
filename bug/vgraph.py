import numpy as np
import itertools
import world,editor,demo

class VizGraph(object):
    def __init__(self):
        self.nodes=[]
        self.near_edeges=[]
        self.edges=[]

    def get_index(self,node_k):
        for i,node_i in enumerate(self.nodes):
            if(node_i[0]==node_k[0] and
                node_i[1]==node_k[1]):
                return i
        return None

    def add_edge(self,edge):
        for x in edge:
            i=self.get_index(x)
            if(i is None):
                size=len(self.nodes)
                self.near_edeges.append([edge])
                self.nodes.append(np.array(x))
            else:
                self.near_edeges[i].append(edge)
        self.edges.append(edge)

    def closest_vertex(self,vertex,world):
        distance=[np.linalg.norm(vertex-node_i) 
                    for node_i in self.nodes]
        for i in np.argsort(distance):
            line_i=(vertex,self.nodes[i])
            if(len(world.collision(line_i))==0):
                return line_i
        raise Exception('should never happen')

    def find_path(self,start,end):
        lines=[]
        current=self.get_index(start)
#        goal
        return lines

def viz_graph(problem):
    graph=VizGraph()
    world=problem.world
    lines= world.all_segments()+list(inter_polgon_vert(world))
    for line_i in lines:        
        if(len(world.collision(line_i))==0):
            graph.add_edge(line_i)
    start=graph.closest_vertex(problem.start,world)
    end=graph.closest_vertex(problem.end,world)
    return [start,end]#graph.edges

def inter_polgon_vert(world):
    indexes=range(len(world))
    pol_pairs=itertools.combinations(indexes,2)
    for i,j in pol_pairs:
        pol_i=world.polygons[i].vertices
        pol_j= world.polygons[j].vertices
        for line_i in itertools.product(pol_i,pol_j):
            yield line_i

def vgraph_loop(in_path):
    problem=world.read_json(in_path)
    controler= demo.AlgControler(problem,viz_graph)
    editor.loop_template(controler)


vgraph_loop("test.json")#"vis.json")
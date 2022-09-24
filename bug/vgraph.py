import numpy as np
import itertools
import world,editor,demo

class VizGraph(object):
    def __init__(self):
        self.nodes=[]
        self.near_edges=[]
        self.edges=[]
    
    def __len__(self):
        return len(self.nodes)

    def get_index(self,node_k):
        for i,node_i in enumerate(self.nodes):
            if(node_i[0]==node_k[0] and
                node_i[1]==node_k[1]):
                return i
        return None

    def add_edge(self,edge):
        for k,x in enumerate(edge):
            t= (k+1)%2
            i=self.get_index(x)
            if(i is None):
                size=len(self.nodes)
                self.near_edges.append([edge[t]])
                self.nodes.append(np.array(x))
            else:
                self.near_edges[i].append(edge[t])
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
        if(type(start)!=int):
            start=self.get_index(start)
        if(type(end)!=int):
            end=self.get_index(end)
        cost=[np.inf for _ in range(len(self))]
        parent=[None for _ in range(len(self))]
        visited=[False for _ in range(len(self))]
        cost[start]=0.0
        active=[start]
        while(active):
            current=active.pop()
            curr_cost=cost[current]
            for edge_i in self.near_edges[current]:
                i=self.get_index(edge_i)
                dist_i=np.linalg.norm(edge_i-curr_cost)
                if(curr_cost+dist_i<cost[i]):
                    cost[i]=curr_cost+dist_i
                    parent[i]=current
                    if(not visited[i]):
                        active.append(i)
            visited[current]=True
        path=[]
        current=end
        while(not (parent[current] is None)):
            line_i=(self.nodes[current],self.nodes[parent[current]])
            path.append(line_i)
            current=parent[current]
        return path

class VizGraphAlg(object):
    def __init__(self):
        self.graph=None

    def __call__(self,problem):
        world=problem.world
        if(self.graph is None):
            self.build_graph()
        start=self.graph.closest_vertex(problem.start,world)
        end=self.graph.closest_vertex(problem.end,world)
        path=self.graph.find_path(start[1],end[1])
        return [start]+path+[end]

    def build_graph(self):
        self.graph=VizGraph()
        lines= world.all_segments()
        lines+=list(inter_polgon_vert(world))
        for line_i in lines:        
            if(len(world.collision(line_i))==0):
                self.graph.add_edge(line_i)

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
    viz_graph=VizGraphAlg()
    controler= demo.AlgControler(problem,viz_graph)
    editor.loop_template(controler)


vgraph_loop("test.json")#"vis.json")
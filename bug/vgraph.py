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
                self.nodes.append(x)
            else:
                self.near_edeges[i].append(edge)
        self.edges.append(edge)

def viz_graph(problem):
    graph=VizGraph()
    world=problem.world
    for line_i in inter_polgon_vert(world):        
        if(len(world.collision(line_i))==0):
            graph.add_edge(line_i)
    return graph.near_edeges[0]

def inter_polgon_vert(world):
    indexes=range(len(world))
    pol_pairs=itertools.combinations(indexes,2)
#    lines=[]
    for i,j in pol_pairs:
        pol_i=world.polygons[i].vertices
        pol_j= world.polygons[j].vertices
        for line_i in itertools.product(pol_i,pol_j):
            yield line_i
#        lines+=list(itertools.product(pol_i,pol_j))
#    return lines

def vgraph_loop(in_path):
    problem=world.read_json(in_path)
    controler= demo.AlgControler(problem,viz_graph)
    editor.loop_template(controler)


vgraph_loop("test.json")#"vis.json")
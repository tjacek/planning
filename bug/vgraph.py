import itertools
import world,editor,demo

def viz_graph(problem):
    world=problem.world
    lines=[line_i 
        for line_i in inter_polgon_vert(world)
          if(len(world.collision(line_i))==0)]
    return lines
#    vertices=world.all_vertices()
#    lines=[]
#    for i,ver_i in enumerate(vertices):
#        for j,ver_j in enumerate(vertices):
#            if(i!=j):
#                line_ij=ver_i,ver_j
#                col=world.collision(line_ij)
#                if(len(col)==0):
#                    lines.append(line_ij)
#    return lines

def inter_polgon_vert(world):
    indexes=range(len(world))
    pol_pairs=itertools.combinations(indexes,2)
    lines=[]
    for i,j in pol_pairs:
        pol_i=world.polygons[i].vertices
        pol_j= world.polygons[j].vertices
        lines+=list(itertools.product(pol_i,pol_j))
    return lines

def vgraph_loop(in_path):
    problem=world.read_json(in_path)
    controler= demo.AlgControler(problem,viz_graph)
    editor.loop_template(controler)


vgraph_loop("test.json")#"vis.json")
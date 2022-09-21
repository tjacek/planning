import world,editor,demo

def viz_graph(problem):
    print(problem)
    vertices=problem.world.all_vertices()
    n_vertices=len(vertices)
    lines=[]
    for i in range(n_vertices):
        for j in range(n_vertices):
            if(i!=j):
                lines.append((vertices[i],vertices[j]))
    return lines

def vgraph_loop(in_path):
    problem=world.read_json(in_path)
    controler= demo.AlgControler(problem,viz_graph)
    editor.loop_template(controler)


vgraph_loop("vis.json")
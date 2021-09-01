import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import plot,states

def plot_problem(problem, path):
    fig=plt.figure() 
    obstacles=problem.collision.obstacles
    plot_objects=[(obstacles,(0,1,0)),( [problem.start.polygon],(0,0,1)),
                    ([problem.end.polygon],(1,0,0))]
    if(type(path)==states.Path):
        points=path.as_points(scale=3.0)
        path=[ (problem.get_state(point_i)[0].polygon,(1,0,1)) for point_i in points]	
    box=problem.get_box()
    fig, ax = plt.subplots()
#    plot_objects+=path
    def animate(i):
        add_objects(ax,path[:i])	
    add_objects(ax,plot_objects)
    plot.set_limit(ax,box.min,box.max)
#    plt.show()
    anim=animation.FuncAnimation(fig,animate,frames=len(path))
    anim.save("test.gif",writer="imagemagick")

def add_objects(ax,plot_objects):
    for pol_i,color_i in plot_objects:
        p_i=plot.to_patches(pol_i,facecolor=color_i)
        ax.add_collection(p_i)

import rapid,square,rrt
problem=square.make_problem()
path=rrt.rdt_search(problem,100)
plot_problem(problem,path)

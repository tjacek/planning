import search,grid
import grid.states as states

class GridSearch(search.FowardSearch):
    def __init__(self,grid,queue=None,gen_pairs=None,):
        super().__init__(states.GridStates(grid,gen_pairs),queue)

    def __call__(self,start,end):
        if(self.problem.grid[end]):
            return False	
        self.problem.goal=self.problem.get_state(end)
        start=self.problem.get_state(start)
        if(hasattr(self.priority_queue, 'set_goal')):
            self.priority_queue.set_goal(self.problem.goal)
        return super().__call__(start)	
    
    def get_plan(self):
        path=[]
        current=self.problem.goal
        while(current):
            path.append(states.cantor_invert(current.id))
            current=current.parent
        path.reverse()
        return path

def save_plan(grid_search,out_path=None):
    grid=grid_search.problem.grid.get_grid()
    plan=grid_search.get_plan()
    for pair_i in plan:
        grid[pair_i]='@'
    text='\n'.join([''.join(row) 
    	                for row in grid])
    if(out_path):
        with open(out_path, "w") as text_file:
            text_file.write(text)
    else:
        print(text)

def get_grid(in_path,grid_type=None):
    gs=grid.read_grid(in_path)
    if(grid_type=="best"):
        q=search.BestFirst(grid.states.distance_heuristic)
    elif(grid_type=="a_star"):
        q=search.AStar(grid.states.distance_heuristic) 
    else:
        q=search.Dijkstra()
    return GridSearch(gs,q)
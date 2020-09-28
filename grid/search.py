import foward,grid
import grid.states as states

class GridSearch(object):
    def __init__(self,grid,queue=None,gen_pairs=None,
                search_type=None):
        self.grid=states.GridStates(grid,gen_pairs)
        if(search_type is None):
            search_type=foward.FowardSearch
        self.search=search_type(self.grid,queue)

    def __call__(self,start,end):
        if(self.grid.grid[end]):
            return False	
        self.grid.goal=self.grid.get_state(end)
        start=self.grid.get_state(start)
        if(hasattr(self.search.priority_queue, 'set_goal')):
            self.search.priority_queue.set_goal(self.grid.goal)
        return self.search(start)	
    
    def get_plan(self):
        path=[]
        current=self.grid.goal
        while(current):
            path.append(states.cantor_invert(current.id))
            current=current.parent
        path.reverse()
        return path

def save_plan(grid_search,out_path=None):
    grid=grid_search.grid.grid.get_grid()
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
    if(grid_type=="depth"):
        q=None	
    elif(grid_type=="breadth"):
        q=foward.FIFO()	
    elif(grid_type=="best"):
        q=foward.BestFirst(grid.states.distance_heuristic)
    elif(grid_type=="a_star"):
        q=foward.AStar(grid.states.distance_heuristic) 
    elif(grid_type=="iter"):
        q=foward.Iterative()
    else:
        q=foward.Dijkstra()
    return GridSearch(gs,q)
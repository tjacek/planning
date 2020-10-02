import foward

class StripsStates(object):
	def __init__(self,world):
		self.world=world
		self.states={}

	def get_first(self):
		first_id=self.world.get_state()
		return self.get_state(first_id)

	def is_goal(self,state_i):
		cond=self.world.goal
		return self.world.check_state(state_i.id,cond)

	def next_state(self,state_i):
		new_states=[]
		for oper_i in self.world.operators:
			cond_i,eff_i=oper_i.precondition,oper_i.effects
			if(self.world.check_state(state_i.id,cond_i)):
				new_id=self.world.new_state(state_i.id,eff_i)
				new_states.append( self.get_state(new_id))
		return new_states

	def get_state(self, state_id):
		if(not state_id in self.states):
			self.states[state_id]=foward.State(state_id)
		return self.states[state_id]

class StripsSearch(object):
	def __init__(self,world,queue=None,
	             search_type=None):
		self.world=StripsStates(world)
		if(search_type is None):
			search_type=foward.FowardSearch
		self.search=search_type(self.world,queue)

	def __call__(self):
		return self.search(self.world.get_first())

	def get_plan(self):
		state_i=self.search.goal_state
		plan=[]
		while(state_i.parent):
			plan.append(state_i.id)
			state_i=state_i.parent
		plan.reverse()
		return plan
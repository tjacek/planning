import sympy 
from sympy.abc import x,y,z

class Variety(object):
	def __init__(self,vars,polynomials,conds):
		self.vars=vars
		self.polynomials=polynomials
		self.conds=conds

	def n_vars(self):
		return len(self.vars)

	def __call__(self,point_i):
		point_dir={ var_j:cord_j
			for var_j,cord_j in zip(self.vars,point_i)}
		values=[pol_i.eval(point_dir) for pol_i in self.polynomials]
		return all([ cond_i(value_i) 
				for value_i,cond_i in zip(values,self.conds)])

def simple_cond(pol_value):
	return pol_value <0
		
def make_pol():
	p0=sympy.Poly(x**2+y**2-1,x,y)
	p1=sympy.Poly(x**2-y,x,y)
	conds=[simple_cond,simple_cond]
	return Variety([x,y],[p0,p1],conds)

if __name__ == "__main__":
	variety=make_pol()
	print(variety([0.5,1]))
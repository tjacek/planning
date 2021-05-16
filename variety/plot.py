import sys
sys.path.append("..")
import sympy
from sympy.plotting import plot_implicit
import variety

def plot2D(variety_i):
	if(variety_i.n_vars()>2):
		raise Exception("Too many vars %d" % variety_i.n_vars())
	plots=[plot_implicit(pol_i.as_expr(),show=False) 
			for pol_i in variety_i.polynomials]
	final_plot=plots[0]
	for plot_i in plots[1:]:
		final_plot.extend(plot_i)
	final_plot.show()

plot2D(variety.make_pol())
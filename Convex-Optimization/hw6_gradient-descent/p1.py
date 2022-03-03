import numpy as np
import gd
import utils


def f(x):
	return 0.5 * x.T@Q@x


def fp(x):
	return Q@x 


def f_2d(x1, x2):
	return 0.5 * gamma * x1**2 + 0.5 * x2**2


# codes for problem (c)
gamma = 0.1
para_stepsize = [2.2, 1, 0.1, 0.01]
Q = np.diag([gamma, 1])
x0 = np.array([1.0, 1.0])
for stepsize in para_stepsize:
	if stepsize == 2.2:
		x_traces = gd.gd_const_ss(fp, x0, stepsize=stepsize, max_iter=20)
	else:
		x_traces = gd.gd_const_ss(fp, x0, stepsize=stepsize)
	print(f'gamma={gamma}, stepsize={stepsize}, number of iterations={len(x_traces)-1}')
	utils.plot_traces_2d(f_2d, x_traces, f'../hw6/figures/gd_traces_gamma{gamma}_ss{stepsize}.pdf')
	utils.plot(f, x_traces, f'../hw6/figures/gd_f_gamma{gamma}_ss{stepsize}.pdf')

# codes for problem (d)
para_gamma = [1, 0.1, 0.01, 0.001]
stepsize=1
for gamma in para_gamma:
	Q = np.diag([gamma, 1])
	x_traces = gd.gd_const_ss(fp, x0, stepsize=stepsize)
	print(f'gamma={gamma}, stepsize={stepsize}, number of iterations={len(x_traces)-1}')

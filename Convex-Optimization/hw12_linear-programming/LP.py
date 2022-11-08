import newton as nt
import numpy as np


def centering_step(c, A, b, x0, t):
	def f(x):
		return c@x - (1/t) * np.sum(np.log(x))

	def fp(x):
		return c - (1/t) * (1/x)

	def fpp(x):
		return (1/t) * np.diag(1/(x**2))

	traces = nt.newton_eq(f, fp, fpp, x0, A, b, initial_stepsize=0.09)
	return traces[-1]


def barrier(c, A, b, x0, tol=1e-8, t0=1, rho=10):
	t = t0
	x = np.array(x0)
	x_traces = [np.array(x0)]
	m = len(x0)
	while t <= m/tol:
		x = centering_step(c, A, b, x, t)
		x_traces.append(x)
		t = t*rho
	return x_traces

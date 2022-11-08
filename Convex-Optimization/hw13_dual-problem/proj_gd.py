import numpy as np


def proj_gd(fp, proj, x0, stepsize, tol=1e-5, maxiter=100000):
	x_traces = [np.array(x0)]
	y_traces = []
	x = np.array(x0)

	for k in range(maxiter):
		y = x-stepsize*fp(x)
		x = proj(y)
		if np.linalg.norm(x_traces[-1]-x) < stepsize * tol:
			break
		y_traces.append(y) # y is output of gradient step before projection
		x_traces.append(np.array(x)) # x is output of projected gradient step

	return x_traces, y_traces

import numpy as np


def newton(fp, fpp, x0, tol=1e-5, maxiter=100000):
	x_traces = []
	x = np.array(x0)
	grad = fp(x)
	hessian = fpp(x)
	iter = 0
	while np.linalg.norm(grad) > tol and iter < maxiter:
		x_traces.append(np.array(x))
		d = np.linalg.solve(hessian, grad)
		x -= d
		grad = fp(x)
		hessian = fpp(x)
	return x_traces 


def damped_newton(f, fp, fpp, x0, alpha=0.5, beta=0.5, tol=1e-5, maxiter=100000):
	x_traces = [np.array(x0)]
	stepsize_traces = []
	tot_num_iter = 0
	x = np.array(x0)
	for it in range(maxiter):
		grad = fp(x)
		if np.linalg.norm(grad) < tol:
			break
		hessian = fpp(x)
		d = np.linalg.solve(hessian, grad)
		d = -1 * d
		stepsize = 1
		fx = f(x)
		alpha_grad_d = alpha * (grad@d)
		while f(x+stepsize * d) > fx + stepsize * alpha_grad_d:
			stepsize *= beta
			tot_num_iter += 1
		x += stepsize * d
		x_traces.append(np.array(x))
		stepsize_traces.append(stepsize)
	return x_traces, stepsize_traces, tot_num_iter

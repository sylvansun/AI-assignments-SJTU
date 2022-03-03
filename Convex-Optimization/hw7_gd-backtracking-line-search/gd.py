import numpy as np


def gd_const_ss(fp, x0, stepsize, tol=1e-5, maxiter=100000):
    x_traces = [np.array(x0)]
    x = np.array(x0)
    for k in range(maxiter):
        grad = fp(x)
        if np.linalg.norm(grad) < tol:
            break
        x -= stepsize * grad
        x_traces.append(np.array(x))
    return x_traces


def gd_armijo(f, fp, x0, initial_stepsize=1.0, alpha=0.5, beta=0.5, tol=1e-5, maxiter=100000):
    stepsize_traces = []
    tot_num_inner_iter = 0
    x = np.array(x0)
    x_traces = [np.array(x)]
    iter=0
    grad=fp(x)
    while np.linalg.norm(grad) >= tol and iter < maxiter:
        iter += 1
        grad = fp(x)
        stepsize = initial_stepsize
        fx = f(x)
        alpha_grad_squared = alpha * (grad @ grad)
        while f(x - stepsize * grad) > fx - stepsize * alpha_grad_squared:
            stepsize *= beta
            tot_num_inner_iter += 1
        x -= stepsize * grad
        x_traces.append(np.array(x))
        stepsize_traces.append(stepsize)
    return x_traces, stepsize_traces, tot_num_inner_iter

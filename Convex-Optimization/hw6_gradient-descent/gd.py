import numpy as np
import math


def norm2(x):  # return the two-norm of a given array. To call this func, x must be np.array
    return math.sqrt(x@x)


def gd_const_ss(fp, x0, stepsize, tol=1e-5, max_iter=100000):
    x = np.array(x0)
    x_traces = [x]
    grad = fp(x)
    norm = norm2(grad)
    grad_norm_traces = [norm]  # saves the sequence of 2-norm of gradient in case we need...
    curr_iter = 0
    while norm > tol and curr_iter < max_iter:
        x = x-stepsize*grad
        x_traces.append(x)
        grad = fp(x)
        norm = norm2(grad)
        grad_norm_traces.append(norm)
        curr_iter = curr_iter+1
    return x_traces

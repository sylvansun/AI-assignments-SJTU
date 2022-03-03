import numpy as np
import newton
import utils
import matplotlib.pyplot as plt


# X: m x 2 matrix, X[i,:] is the 2D feature vector of the i-th sample
X = np.array([[1,1.5], 
			  [1.2, 2.5], 
			  [1,3.5], 
			  [2,2.25], 
			  [1.8, 3], 
			  [2.5,4], 
			  [3,1.9], 
	          [1.5, .5], 
	          [2.5, .8], 
	          [2.8, .3], 
	          [3.2, .3], 
	          [3, .8], 
	          [3.8, 1], 
	          [4,2], 
	          [1.8,1.8]])
# y: m-D vector, y[i] is the label of the i-th sample
y = np.append(np.ones((7,)), -np.ones((8,)))

# append a constant 1 to each feature vector, so X is now a m x 3 matrix
X = np.append(X, np.ones((15,1)), axis=1)

# Xy[i,:] = X[i,:] * y[i]
Xy = X * y.reshape((-1,1))
# X.shape = (15,3), Xy.shape = (15, 3), y.shape = (15,)


# sigmoid function
def sigmoid(z):
	return 1.0 / (1 + np.exp(-z))


def sigmoid_p(z):
	s = sigmoid(z)
	return s * (1 - s)


def f(w):
	return -np.sum(np.log(sigmoid(Xy@w)))


def fp(w):
	return -(1-sigmoid(Xy@w)) @ Xy


def fpp(w):
	return (X.T*sigmoid_p(Xy@w))@X  # X.T*sigmoid_p uses broadcasting mechanism, here the result is 3*3


# minimize f by damped Newton
w0 = np.array([1.0,1.0,0.0])
path = '../hw8/figures/'

w_traces, stepsize_traces, num_iter_inner = newton.damped_newton(f, fp, fpp, w0, alpha=0.1, beta=0.7)
ws = w_traces[-1]
fs = f(ws)

print()
print("Damped Newton's method")
print('  number of iterations in outer loop:', len(w_traces)-1)
print('  total number of iterations in inner loop:', num_iter_inner)
print('  solution:', ws)
print('  value:', fs)


def gap(w):
	return f(w) - fs


utils.plot(gap, w_traces, path+'dnt_gap.pdf')
fig = plt.figure(figsize=(3.5,2.5))
plt.plot(stepsize_traces, '-o', color='blue')
plt.xlabel('iteration (k)')
plt.ylabel('stepsize')
plt.tight_layout(pad=0.1)
fig.savefig(path+'dnt_ss.pdf')

# try using pure Newton but failed
# another_traces = newton.newton(fp, fpp, w0)
"""
If we use pure Newton's method with the same w0, we cannot get a inverse Hessian Matrix because it is singular......
Try using some other initial values, and the Newton's method does work sometimes.
For detailed explanation, please read the pdf file for this homework assignment.. ^_^
"""
# This is an example where pure Newton's method actually works
new_traces = newton.newton(fp, fpp, np.array([-1.5,2.5,-2.5]))
f_value = f(new_traces[-1])
print()
print("Newton's method with w0=(-1.0,3.0,-3.0)")
print('  number of iterations:', len(new_traces)-1)
print('  solution:', new_traces[-1])
print('  value:', f_value)
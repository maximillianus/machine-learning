"""
This is an algorithm script to implement gradient descent from scratch in
Python. This script is meant to illustrate how gradient descent optimizes and finds
the minimum of a function
"""

import numpy as np
import matplotlib.pyplot as plt

# Functions to draw

def draw_gradient_descent(iters_list, step_list):
    try:
        plt.plot(iters_list, step_list)
    except Exception as e:
        print(e)
        raise
    else:
        plt.show()

def draw_function(f):
    x = np.arange(1,5)
    y = f(x)
    dy_dx = np.gradient(y)
    try:
        plt.plot(x,y)
        plt.plot(x,dy_dx)
    except Exception as e:
        print(e)
        raise
    else:
        plt.show()

# example cost function
"""
Function can't be linear function like y = 2*x since the gradient will
always be constant and thus cannot be reduced to 0
"""
f_x = lambda x: (x - 3) ** 2
df_x = lambda x: x * (x - 3)

# gradient descent formula
"""
* Initial current x will be arbitrary choice. Next cur_x will depend on
the previous calculation.
* Rate is learning rate and it will be constant
* dy_dx will change depending on the cur_x. The closer we are to
local/global minima, the smaller dy_dx will be.
"""
def calc_new_x(cur_x, rate, dy_dx):
    return cur_x - ( rate * dy_dx(cur_x) )

# Initate gradient descent
## Setup parameters

x_0 = 2    # initial x position is random/arbitrary
iters = 0; max_iters=1000
iters_list = []
learning_rate = 0.01
precision = 0.0001  # the minimum difference the step size have to be before we quit the loop
step_size = 10
step_size_list = []
while step_size > precision and iters < max_iters:
    # This loop will quit if step_size is > precision
    # and/or iters exceed max iteration needed
    print('Iteration:', iters)
    # define what prev x is. for 1st iteration, prev_x = x_0
    prev_x = x_0
    # calc what cur_x will be
    x_0 = calc_new_x(prev_x, learning_rate, df_x)
    # calculate step_size to know how 'steep' we are descending
    # stop when step_size < precision we need
    step_size = abs(x_0 - prev_x)
    print('Prev_x:', prev_x, '| Curr_x:', x_0, '| Step Size:', round(step_size, 5))
    iters_list.append(iters)
    step_size_list.append(step_size)
    iters += 1

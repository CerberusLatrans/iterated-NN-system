import numpy as np
from random import random
from plotly_plotting import plot_ifs_2d, plot_ifs_3d
from iter_funcs import barnsley_fern, barnsley_fern_3d, rand_func, serpinski_carpet, nn_to_iter_func
from plt_plotting import graph_2d, graph_2d_iter
from model import IterNet2D
import torch

"""
Ideas:
Use neural net to simulate dynamical system (chaos learned）
Iterated linear function system: 
    Use neural net to generate continuous space of affine transforms (6 output nodes)
    input is a random number 0-1
Iterated non-linear function system:
    Use neural net to generate new point given an existing point
    (may not work if IFS is supposed to be ignorant of current point)
"""
def generate(f, max_iter=10000, x0=np.array([0, 0])):
    x = x0
    for n in range(max_iter):
        yield x
        #random num 0-1
        # apply output
        x = f(x)
        



n = 100000
#generator_2d = generate(serpinski_carpet, max_iter=n)
#plot_ifs_2d(generator_2d)
#generator_3d = generate(barnsley_fern_3d, max_iter=1000, x0=np.array([0, 0, 0]))
#plot_ifs_3d(generator_3d)

model = IterNet2D()
model.load_state_dict(torch.load("weights"))
generator_2d = generate(nn_to_iter_func(model), max_iter=n)
plot_ifs_2d(generator_2d)
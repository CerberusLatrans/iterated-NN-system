import numpy as np
from random import random
import random as rdm
import math
import torch.nn as nn
import torch

def barnsley_fern(x):
    r = random()
    #r = min(max(np.random.normal(loc=0.5, scale=0.25), 0), 1)
    #r = min(max(np.random.normal(loc=1, scale=1), 0), 1)
    A = np.array([[1, 0],
                  [0, 1]])
    b = np.array([0, 0])
    
    if r < 0.01:
        A = np.array([[0, 0],
                      [0, 0.16]])
    elif r < 0.86:
        A = np.array([[0.85, 0.04],
                      [-0.04, 0.85]])
        b = np.array([0, 1.60])
    elif r < 0.93:
        A = np.array([[0.20, -0.26],
                      [0.23, 0.22]])
        b = np.array([0, 1.60])
    else:
        A = np.array([[-0.15, 0.28],
                      [0.26, 0.24]])
        b = np.array([0, 0.44])

    y = A@x + b
    return y

def barnsley_fern_3d(x):
    r = random()

    A = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]])
    b = np.array([0, 0, 0])
    
    if r < 0.01:
        A = np.array([[0, 0, 0],
                      [0, 0.16, 0],
                      [0, 0, 0.16]])
    elif r < 0.86:
        A = np.array([[0.85, 0.04, 0.04],
                      [-0.04, 0.85, 0.04],
                      [-0.04, -0.04, 0.85]])
        
        b = np.array([0, 1.60, 0])
    elif r < 0.93:
        A = np.array([[0.20, -0.26, -0.26],
                      [0.23, 0.22, -0.26],
                      [0.23, 0.23, 0.24]])
        b = np.array([0, 1.60, 0])
    else:
        A = np.array([[-0.15, 0.28, 0.28],
                      [0.26, 0.24, 0.28],
                      [0.26, 0.26, 0.39]])
        b = np.array([0, 0.44, 0])

    y = A@x + b
    return y

def serpinski_carpet(x):
    idx = rdm.randrange(0,8)
    a = [0, 0, 0, 1/3, 1/3, 2/3, 2/3, 2/3]
    b = [0, 1/3, 2/3, 0, 2/3, 0, 1/3, 2/3]
    return x*(1/3) + np.array([a[idx], b[idx]])

def rand_func(x):
    A = np.array([[random(), random()],
                  [random(), random()]])
    b = np.array([random(), random()]) 
    y = A@x + b
    return y

def nn_to_iter_func(model):
    def nn(x):
        r = torch.tensor([random()])
        out = model(r).detach().numpy()
        A = np.array([[out[0], out[1]],
                      [out[2], out[3]]])
        b = np.array([out[4], out[5]]) 
        ret = A@x + b
        return ret
    return nn

def transform_to_points(func, n, p0=np.array([0, 0])):
    #maybe always make the previous point be from the ground truth?
    seeds = np.random.rand(n)
    if isinstance(func, nn.Module):
        transforms = func(torch.unsqueeze(torch.Tensor(seeds), 1)).detach().numpy()
    else:
        transforms = np.array([func(x) for x in seeds])
    
    points = []
    p=p0
    for i in range(n):
        points.append(p)
        trans = transforms[i]
        A = np.array([[trans[0], trans[1]],
                      [trans[2], trans[3]]])
        b = np.array([trans[4], trans[5]]) 
        p = A@p + b

    return np.array(points)   

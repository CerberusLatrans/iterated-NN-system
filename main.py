from plotly import graph_objects as go
import numpy as np
from random import random

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
        x = f(x, random())
        

def barnsley_fern(x, r):
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

def rand_func(x, r):
    A = np.array([[random(), random()],
                  [random(), random()]])
    b = np.array([random(), random()]) 
    y = A@x + b
    return y


def barnsley_fern_3d(x, r):
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

#generator_2d = generate(barnsley_fern, max_iter=10000)

def plot_ifs_2d(generator):
    points = [x for x in generator]
    #points = np.fromiter(generator, np.dtype((float, 2)))
    points = np.transpose(points)
    fig = go.Figure(data=go.Scatter(
        x=points[0],
        y=points[1],
        mode="markers",
        marker_color = "black",
        marker_size = 2,
    ))

    fig.show()

def plot_ifs_3d(generator):
    points = [x for x in generator]
    #points = np.fromiter(generator, np.dtype((float, 2)))
    points = np.transpose(points)
    fig = go.Figure(data=go.Scatter3d(
        x=points[0],
        y=points[1],
        z=points[2],
        mode="markers",
        marker_color = "black",
        marker_size = 2,
    ))

    fig.show()

generator_3d = generate(barnsley_fern_3d, max_iter=10000, x0=np.array([0, 0, 0]))
plot_ifs_3d(generator_3d)
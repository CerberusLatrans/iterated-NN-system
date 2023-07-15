import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def graph_2d(generator):
    fig, ax = plt.subplots()
    for [x,y] in generator:
        plt.scatter(x, y, marker='o') 
    plt.show()

def graph_2d_iter(generator, n):
    fig, ax = plt.subplots()
    plt.xlim(-20, 20)
    plt.ylim(-20,20)
    scat = plt.plot([], [], 'o')

    xs = []
    ys = []

    def init():
        scat.set_offsets([])
        return scat,

    def update(i):
        print(i)
        x = next(generator)
        print(x)
        xs.append(x[0])
        ys.append(x[1])
        print(scat)
        scat.set_data(xs, ys)
        return scat,

    ani = FuncAnimation(fig, update, frames=n, blit=True, repeat=False)
    plt.show()

from system.leaves import SQUARE, FERN2D
from ifs import markov_chooser, iterate
from visualize import render_points
import numpy as np


mkv_1 = [[0.3, 0.5, 0.1, 0.1],
         [0.1, 0.5, 0.4, 0.0],
         [0.3, 0.3, 0.2, 0.2],
         [0.25, 0.25, 0.25, 0.25]]
mkv_2 = np.divide((mx:=np.random.rand(4,4)), np.reshape(mx.sum(axis=1), (4,1)))
mkv_3 = np.divide((mx:=np.random.rand(4,4)), np.reshape(mx.sum(axis=1), (4,1)))
mkv_4 = np.divide((mx:=np.random.rand(4,4)), np.reshape(mx.sum(axis=1), (4,1)))
         
#render_points(iterate(markov_chooser(SQUARE,mkv_1), max_iter=20000),show=True)
#render_points(iterate(markov_chooser(SQUARE,mkv_2), max_iter=20000),show=True)
#render_points(iterate(markov_chooser(SQUARE,mkv_3), max_iter=20000),show=True)
#render_points(iterate(markov_chooser(SQUARE,mkv_4), max_iter=20000),show=True)

render_points(iterate(markov_chooser(FERN2D, mkv_1), max_iter=50000), show=True, dim=(400,400))

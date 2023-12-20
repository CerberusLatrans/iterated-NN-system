import numpy as np

from ifs import iterate, iterate_indexed
from markov import markov_chooser, markov_indexer, weighted_random_chooser
from visualize import render_points, ColorScheme
from catalogue.leaves import SQUARE, FERN2D
from catalogue.chains import EHRENFEST, UNIFORM, EHRENFEST2, ABSORBING, ERG_REG_1, AREA_WEIGHTED, ERG_REG_SUM_1, RIGHT_TO_MAIN_MISSING, MAIN_TO_RIGHT_MISSING, MAIN_TO_MAIN_MISSING


mkv_1 = [[0.3, 0.5, 0.1, 0.1],
         [0.1, 0.5, 0.4, 0.0],
         [0.3, 0.3, 0.2, 0.2],
         [0.25, 0.25, 0.25, 0.25]]
mkv_2 = np.divide((mx:=np.random.rand(4,4)), np.reshape(mx.sum(axis=1), (4,1)))
mkv_3 = np.divide((mx:=np.random.rand(4,4)), np.reshape(mx.sum(axis=1), (4,1)))
mkv_4 = np.divide((mx:=np.random.rand(4,4)), np.reshape(mx.sum(axis=1), (4,1)))
         
#render_points(iterate(markov_chooser(SQUARE,mkv_1), num_iters=20000),show=True)
#render_points(iterate(markov_chooser(SQUARE,mkv_2), num_iters=20000),show=True)
#render_points(iterate(markov_chooser(SQUARE,mkv_3), num_iters=20000),show=True)
#render_points(iterate(markov_chooser(SQUARE,mkv_4), num_iters=20000),show=True)
absorbing = [[0.85, 0.05, 0.05, 0.05],
         [0.1, 0.5, 0.4, 0.0],
         [0.3, 0.3, 0.2, 0.2],
         [0.25, 0.25, 0.25, 0.25]]
render_points(iterate(weighted_random_chooser(FERN2D), num_iters=50000), show=True, dim=(500,500))


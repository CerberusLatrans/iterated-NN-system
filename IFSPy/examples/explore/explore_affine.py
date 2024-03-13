import numpy as np
from catalogue.leaves import FERN2D, MAPLE2D
from catalogue.shapes import SQUARE
from catalogue.chains import AREA_WEIGHTED
from ifs import iterate, ifs_interpolate, iterate_indexed
from markov import weighted_random_chooser, markov_indexer
from visualize import render_transforms, render_points, render_gif, ColorScheme
from affine import Transformations as T

IMG_PATH = 'examples/explore/affine_explore_images/'
PATH_LENGTH = 20

MIDPOINT = FERN2D
LOWER = np.array([MIDPOINT[0], T.translate(MIDPOINT[1], (0, -5)), MIDPOINT[2], MIDPOINT[3]])
UPPER = np.array([MIDPOINT[0], T.translate(MIDPOINT[1], (0, 5)), MIDPOINT[2], MIDPOINT[3]]) 

NAME = 'main_translate_vert'

#ifs_list = [np.random.uniform(LOWER, UPPER, (4,3,3)) for _ in range(PATH_LENGTH)]
ifs_path = ifs_interpolate(LOWER, UPPER, t=100)
transforms_frames = [render_transforms(ifs) for ifs in ifs_path]
render_gif(transforms_frames,
           fpath=IMG_PATH+f'{NAME}.gif',
           image_mode=True,
           duration=10,
           show=False)

#np.save('explore_main_b', np.asarray(ifs_list))

attractors_points_idxs = [iterate_indexed(markov_indexer(AREA_WEIGHTED(ifs)), ifs) for ifs in ifs_path]
attractors_points = [x[0] for x in attractors_points_idxs]
attractors_idxs = [x[1] for x in attractors_points_idxs]
render_gif(attractors_points,
           fpath=IMG_PATH+f'{NAME}_attractors.gif',
           image_mode=False,
           indices_sequence=attractors_idxs,
           show=False,
           color_scheme=ColorScheme.TRANSFORM)

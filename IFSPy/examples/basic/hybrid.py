from catalogue.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN, random_ifs
from ifs import iterate, closest_mapping, ifs_weighted_sum, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms
import numpy as np

hybrid = ifs_weighted_sum([MAPLE2D, CYCLO_FERN])
attractor = iterate(hybrid, num_iters=20000)
render_points(attractor, show=True)
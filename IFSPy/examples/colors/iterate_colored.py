from visualize import render_points, ColorScheme
from ifs import iterate_indexed
from chains import AREA_WEIGHTED, MAIN_TO_RIGHT_MISSING, RIGHT_TO_MAIN_MISSING, MAIN_TO_MAIN_MISSING
from system.leaves import FERN2D, SQUARE, MAPLE2D
from markov import markov_indexer
import matplotlib as mpl

ifs_obj = FERN2D
mkv = MAIN_TO_MAIN_MISSING #AREA_WEIGHTED(ifs_obj)
attractor, idxs = iterate_indexed(
                            markov_indexer(mkv),
                            ifs_obj,
                            max_iter=100000)
render_points(attractor, show=True, dim=(1000,1000),
              color_scheme=ColorScheme.TRANSFORM, indices=idxs, cmap=mpl.colormaps['viridis'])
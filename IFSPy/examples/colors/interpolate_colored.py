from system.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN
from ifs import iterate_indexed, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms, ColorScheme
from markov import markov_interpolate, markov_indexer
from chains import AREA_WEIGHTED
import numpy as np

def main():
    ifs_sequence = ifs_interpolate_series([FERN2D, MAPLE2D], t=20, mappings=[[0,1,2,3]])
    attractors_idxs = [iterate_indexed(markov_indexer(AREA_WEIGHTED(x)), x, max_iter=20000) for x in ifs_sequence]
    attractors, indices = [a for a,i in attractors_idxs], [i for a,i in attractors_idxs]
    render_gif(attractors, fpath="fern_to_maple2.gif",show=True, duration=100,
               dim=(400,400),color_scheme=ColorScheme.TRANSFORM, indices_sequence=indices)
if __name__ == "__main__":
    main()
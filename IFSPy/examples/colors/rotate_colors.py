from system.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN
from ifs import iterate_indexed, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms, ColorScheme
from markov import markov_interpolate, markov_indexer
from chains import AREA_WEIGHTED
import numpy as np

def main():
    #each step shows another layer of self-similarity
    obj = MAPLE2D
    attractor, idxs = iterate_indexed(markov_indexer(AREA_WEIGHTED(obj)), obj, max_iter=100000)
    attractors, indices = [], []
    for i in range(20):
        attractors.append(attractor)
        indices.append(idxs)
        idxs = idxs[-1:] + idxs[:-1]
        #idxs = idxs[1:]+idxs[:1]
    render_gif(attractors, fpath="rotate_maple_colors.gif",show=True, duration=400,
               dim=(500,500),color_scheme=ColorScheme.TRANSFORM, indices_sequence=indices)
if __name__ == "__main__":
    main()
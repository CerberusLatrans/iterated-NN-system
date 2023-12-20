from catalogue.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN, random_ifs
from ifs import iterate, closest_mapping, ifs_weighted_sum, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms
import numpy as np

def main():
    leaves = [FERN2D, MAPLE2D, CYCLO_FERN]
    steps = 10
    leaf_sequence = []
    for i in range(steps):
        if i%2==0:
            hybrid = ifs_weighted_sum(leaves, np.random.rand(len(leaves)))
        else:
            hybrid = random_ifs(4)
        leaf_sequence.append(hybrid)
    ifs_sequence = ifs_interpolate_series(leaf_sequence, t=10)
    attractors = [iterate(ifs, num_iters=20000) for ifs in ifs_sequence]
    render_gif(attractors, dim=(400,400),fpath="wander.gif",show=True, duration=100)
if __name__ == "__main__":
    main()
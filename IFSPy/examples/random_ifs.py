from system.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN, random_ifs
from ifs import iterate, closest_mapping, ifs_weighted_sum, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms
import numpy as np
from tqdm import tqdm

def main():
    steps = 5
    n_codes = 20
    leaf_sequence = []
    for i in range(steps):
        hybrid = random_ifs(n_codes)
        leaf_sequence.append(hybrid)
    ifs_sequence = ifs_interpolate_series(leaf_sequence, mappings =np.full((steps-1,n_codes), range(n_codes)), t=10)
    attractors = []
    for ifs in tqdm(ifs_sequence, desc="Iterating..."):
        attractors.append(iterate(ifs, max_iter=20000))
    render_gif(attractors, dim=(400,400),fpath=f"{n_codes}_codes_random_seq.gif",show=True, duration=100)
if __name__ == "__main__":
    main()
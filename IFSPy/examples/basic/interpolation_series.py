from catalogue.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN
from ifs import iterate, closest_mapping, ifs_weighted_sum, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms

def main():
    ifs_sequence = ifs_interpolate_series([FERN2D, MAPLE2D, CYCLO_FERN, FERN2D], t=10)
    attractors = [iterate(ifs, num_iters=20000) for ifs in ifs_sequence]
    render_gif(attractors, dim=(400,400),fpath="interpolation_series.gif",show=True, duration=100)
if __name__ == "__main__":
    main()
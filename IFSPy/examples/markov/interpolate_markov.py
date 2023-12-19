from system.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN
from ifs import iterate, markov_chooser
from visualize import render_points, render_gif, render_transforms
from markov import markov_interpolate, EHRENFEST, UNIFORM, AREA_WEIGHTED, IDENTITY, MAIN_TO_RIGHT_MISSING, RIGHT_TO_MAIN_MISSING

def main():
    markovs = markov_interpolate(RIGHT_TO_MAIN_MISSING, MAIN_TO_RIGHT_MISSING, t=20)
    choosers = [markov_chooser(FERN2D, mkv) for mkv in markovs]
    attractors = [iterate(ch, max_iter=50000) for ch in choosers]
    render_gif(attractors, dim=(500,500),fpath="main_right_missing_interpolation.gif",show=True, duration=100)
if __name__ == "__main__":
    main()
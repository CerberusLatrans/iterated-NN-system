from system.leaves import FERN2D, MAPLE2D
from ifs import iterate, get_probabilities, random_choice, ifs_interpolate
from visualize import render_points, render_points_sequence

def main():
    
    t = 10
    ifs_sequence = ifs_interpolate(FERN2D, MAPLE2D, t=t)
    attractors = [iterate(ifs, max_iter=2000) for ifs in ifs_sequence]
    render_points_sequence(attractors, show=True, fpath="test.gif")
    #render_transforms(MAPLE2D, show=True)
if __name__ == "__main__":
    main()
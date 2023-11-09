from system.leaves import FERN2D, MAPLE2D
from ifs import iterate, get_probabilities, random_choice, ifs_interpolate
from visualize import render_points, render_points_sequence
import itertools

def main():
    t = 20
    for permutation in itertools.permutations(range(len(FERN2D))):
        ifs_sequence = ifs_interpolate(FERN2D, MAPLE2D, mapping=permutation,t=t)
        attractors = [iterate(ifs, max_iter=20000) for ifs in ifs_sequence]
        render_points_sequence(attractors, dim=(400,400),show=True, fpath=f"{permutation}.gif")
if __name__ == "__main__":
    main()
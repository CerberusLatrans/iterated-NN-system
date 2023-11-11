from system.leaves import FERN2D, MAPLE2D, SQUARE
from ifs import iterate, ifs_interpolate, closest_mapping, ifs_weighted_sum
from visualize import render_points, render_points_sequence, render_transforms

def main():
    #print(closest_mapping(FERN2D, SQUARE))
    #print(closest_mapping(MAPLE2D, SQUARE))
    #render_transforms(SQUARE, show=False)
    #render_transforms(MAPLE2D, show=True)
    t = 20
    combined_ifs = ifs_weighted_sum([FERN2D,MAPLE2D, SQUARE], weights=[0.495, 0.495,0.01])
    render_points(iterate(combined_ifs, max_iter=2000), dim=(100,100),show=True)
    """ifs_sequence = ifs_interpolate(FERN2D, SQUARE,t=t, mapping=[0,3,2,1])
    ifs_sequence = ifs_interpolate(FERN2D, MAPLE2D,t=t, mapping=None)
    attractors = [iterate(ifs, max_iter=20000) for ifs in ifs_sequence]
    render_points_sequence(attractors, dim=(400,400),fpath="test.gif",show=True)"""
if __name__ == "__main__":
    main()
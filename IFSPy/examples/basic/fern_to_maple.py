from system.leaves import FERN2D, MAPLE2D, SQUARE, CYCLO_FERN, random_ifs
from ifs import iterate, closest_mapping, ifs_weighted_sum, ifs_interpolate_series
from visualize import render_points, render_gif, render_transforms
import numpy as np
from tqdm import tqdm

def main():
   """render_transforms(FERN2D).convert('RGB').save('fern1transforms.png')
   render_transforms(CYCLO_FERN).convert('RGB').save('fern2transforms.png')
   render_transforms(MAPLE2D).convert('RGB').save('mapletransforms.png')

   fern = render_points(iterate(FERN2D, max_iter=100000),show=True, dim=(400,400))
   fern2 = render_points(iterate(CYCLO_FERN, max_iter=100000),show=True, dim=(400,400))
   maple = render_points(iterate(MAPLE2D, max_iter=100000),show=True, dim=(400,400))
   
   fern.convert('RGB').save("fern1.png")
   fern2.convert('RGB').save("fern2.png")
   maple.convert('RGB').save("maple.png")"""

   ifs_sequence = ifs_interpolate_series([FERN2D, MAPLE2D], t=10, mappings=[[0,1,3,2]])
   attractors = [iterate(ifs, max_iter=20000) for ifs in ifs_sequence]
   render_gif(attractors, dim=(400,400),fpath="fern_to_maple2.gif",show=True, duration=100)

if __name__ == "__main__":
    main()
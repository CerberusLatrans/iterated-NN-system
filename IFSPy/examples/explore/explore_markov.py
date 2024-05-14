import numpy as np
from catalogue.leaves import FERN2D, MAPLE2D, CYCLO_FERN
from catalogue.shapes import SQUARE
from ifs import iterate, iterate_indexed
from visualize import render_points, render_gif, render_transforms, ColorScheme
from markov import markov_interpolate, markov_indexer
from catalogue.chains import AREA_WEIGHTED

IMG_PATH = 'examples/explore/markov_explore_images/fern/one_zero/'

IFS = FERN2D
def drain(markov_row, idx):
    new_row = np.concatenate((markov_row[:idx], [0], markov_row[idx+1:]))
    return new_row/new_row.sum()
MIDPOINT_MARKOV = AREA_WEIGHTED(IFS)
ROW = MIDPOINT_MARKOV[0]
names = {0:'stem', 1:'main', 2:'left', 3:'right'}
#names = {0:'bl', 1:'br', 2:'tl', 3:'tr'}
for i in range(4):
    for j in range(4):
        drained_markov = np.concatenate(
            (MIDPOINT_MARKOV[:i],
            [drain(MIDPOINT_MARKOV[i], j)],
            MIDPOINT_MARKOV[i+1:]))
        print(drained_markov)
        attractor, idxs = iterate_indexed(
            markov_indexer(drained_markov), IFS, num_iters=100000)
        fpath = IMG_PATH + f"{names[i]}_to_{names[j]}_drained.png"
        render_points(attractor,
                      dim=(400,400),
                      color_scheme=ColorScheme.TRANSFORM,
                      indices=idxs,
                      fpath=fpath)

"""from itertools import permutations
for perm in permutations([0,1,2,3]):
    drained_markov = np.concatenate(
        ([drain(ROW, perm[0])],
         [drain(ROW, perm[1])],
         [drain(ROW, perm[2])],
         [drain(ROW, perm[3])]))
    print(drained_markov)
    attractor, idxs = iterate_indexed(
        markov_indexer(drained_markov), IFS, num_iters=100000)
    fpath = IMG_PATH + "{}_{}_{}_{}_drained.png".format(*[names[i]+"-"+names[x] for i,x in enumerate(perm)])
    render_points(attractor,
                  dim=(400,400),
                  color_scheme=ColorScheme.TRANSFORM,
                  indices=idxs,
                  fpath=fpath)"""
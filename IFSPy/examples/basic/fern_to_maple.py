from catalogue.leaves import FERN2D, MAPLE2D
from ifs import iterate, ifs_interpolate
from visualize import render_gif
from markov import weighted_random_chooser
from tqdm import tqdm

"""render_transforms(FERN2D).convert('RGB').save('fern1transforms.png')
render_transforms(CYCLO_FERN).convert('RGB').save('fern2transforms.png')
render_transforms(MAPLE2D).convert('RGB').save('mapletransforms.png')
fern = render_points(iterate(FERN2D, num_iters=100000),show=True, dim=(400,400))
fern2 = render_points(iterate(CYCLO_FERN, num_iters=100000),show=True, dim=(400,400))
maple = render_points(iterate(MAPLE2D, num_iters=100000),show=True, dim=(400,400))

fern.convert('RGB').save("fern1.png")
fern2.convert('RGB').save("fern2.png")
maple.convert('RGB').save("maple.png")"""

ifs_sequence = ifs_interpolate(FERN2D, MAPLE2D, t=50, mapping=None, target_start=-5, target_end=5)
attractors = [iterate(weighted_random_chooser(ifs), num_iters=20000) for ifs in ifs_sequence]
render_gif(attractors, dim=(400,400),
           fpath="./IFSPy/examples/basic/images/way_beyond_interpolate.gif",
           show=True, duration=100)
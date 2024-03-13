import numpy as np
import matplotlib.pyplot as plt
import pyswarms as psw
from pyswarms.utils.plotters import plot_cost_history, plot_contour, plot_surface
from pyswarms.utils.plotters.formatters import Mesher

from optimize_ifs import get_bounds, space_to_affine_dim, get_obj_func, particle_to_transforms, transforms_to_particle
from catalogue.leaves import FERN2D, MAPLE2D
from catalogue.shapes import SQUARE
from ifs import iterate
from markov import weighted_random_chooser
from visualize import render_transforms, render_points, render_gif
from objective import hutchinson

# Set-up hyperparameters
options = {'c1': 0.9, 'c2': 0.5, 'w':0.90}
SPACE_DIM = 2
N_TRANSFORMS = 4
A_BOUNDS = (-0.3,0.3)
B_BOUNDS = (-0.3,0.3)
TARGET_IFS = FERN2D
print(transforms_to_particle(TARGET_IFS))
# Call instance of PSO
PSO_DIM = N_TRANSFORMS*space_to_affine_dim(SPACE_DIM)
BOUNDS = get_bounds(reference=FERN2D, a_bounds=A_BOUNDS, b_bounds=B_BOUNDS, space_dim=SPACE_DIM, n_transforms=N_TRANSFORMS)
optimizer = psw.single.GlobalBestPSO(n_particles=20,
                                     dimensions=PSO_DIM,
                                     options=options,
                                     bounds=BOUNDS)

target = iterate(weighted_random_chooser(TARGET_IFS), num_iters=1000)
#render_points(target, show=True)

# Perform optimization
obj_func = get_obj_func(target)
cost, winner = optimizer.optimize(obj_func, iters=50)
print("WINNER: ", winner)
history = np.array(optimizer.pos_history)
differences = np.sum(np.abs(history - transforms_to_particle(TARGET_IFS)), axis=-1)
plt.plot(differences)
plt.show()

winner_idx = (np.where(winner==history)[0][0], np.where(winner==history)[1][0]) 
print(history[:winner_idx[0]+1,winner_idx[1],:].shape)

ifs_list = [particle_to_transforms(p) for p in history[:winner_idx[0]+1, winner_idx[1], :]]
transforms_frames = [render_transforms(ifs) for ifs in ifs_list]
render_gif(transforms_frames, fpath='optimize_ifs_transforms3.gif', image_mode=True, show=True)

np.save('optimize_ifs_transforms', np.asarray(ifs_list))

attractors_frames = [iterate(weighted_random_chooser(ifs)) for ifs in ifs_list]
render_gif(attractors_frames, fpath='optimize_ifs_attractors3.gif', image_mode=False, show=True)

"""ifs = particle_to_transforms(winner)
render_transforms(ifs, show=True)
collage = hutchinson(ifs, target)
render_points(collage, show=True)
attractor = iterate(weighted_random_chooser(ifs))
render_points(attractor, show=True)"""
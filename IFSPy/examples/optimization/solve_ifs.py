import numpy as np
import matplotlib.pyplot as plt
import pyswarms as psw
from pyswarms.utils.plotters import plot_cost_history, plot_contour, plot_surface
from pyswarms.utils.plotters.formatters import Mesher

from optimize_ifs import get_bounds, space_to_affine_dim, get_obj_func, particle_to_transforms, transforms_to_particle
from catalogue.leaves import FERN2D
from catalogue.shapes import SQUARE
from ifs import iterate
from markov import weighted_random_chooser
from visualize import render_transforms, render_points, render_gif
from objective import hutchinson

# Set-up hyperparameters
options = {'c1': 0.3, 'c2': 0.5, 'w':0.8}
SPACE_DIM = 2
N_TRANSFORMS = 4
A_BOUNDS = (-1,1)
B_BOUNDS = (-2,2)

# Call instance of PSO
PSO_DIM = N_TRANSFORMS*space_to_affine_dim(SPACE_DIM)
BOUNDS = get_bounds(a_bounds=A_BOUNDS, b_bounds=B_BOUNDS, space_dim=SPACE_DIM, n_transforms=N_TRANSFORMS)
optimizer = psw.single.GlobalBestPSO(n_particles=20,
                                     dimensions=PSO_DIM,
                                     options=options,
                                     bounds=BOUNDS)

TARGET_IFS = FERN2D
target = iterate(weighted_random_chooser(TARGET_IFS), num_iters=10)
render_points(target, show=True)

# Perform optimization
obj_func = get_obj_func(target)
cost, winner = optimizer.optimize(obj_func, iters=100)
history = np.array(optimizer.pos_history)
print(history.shape)
differences = np.sum(np.abs(history - transforms_to_particle(TARGET_IFS)), axis=-1)
print(differences.shape)
plt.plot(differences)
plt.show()

transforms_frames = [render_transforms(particle_to_transforms(p)) for p in history]
render_gif(transforms_frames, show=True)

ifs = particle_to_transforms(winner)
render_transforms(ifs, show=True)
collage = hutchinson(ifs, target)
render_points(collage, show=True)
attractor = iterate(weighted_random_chooser(ifs))
render_points(attractor, show=True)
import numpy as np
import matplotlib.pyplot as plt
import pyswarms as psw
from pyswarms.utils.plotters import plot_cost_history

from optimize_markov import get_bounds, get_obj_func, particle_to_markov
from catalogue.leaves import FERN2D
from catalogue.shapes import SQUARE
from ifs import iterate
from markov import determinant_probabilities, markov_chooser
from visualize import render_points

# Set-up hyperparameters
options = {'c1': 0.3, 'c2': 0.5, 'w':0.8}
N_TRANSFORMS = 4
BOUNDS = get_bounds((0,1), N_TRANSFORMS)

# Call instance of PSO
optimizer = psw.single.GlobalBestPSO(n_particles=20,
                                     dimensions=N_TRANSFORMS**2,
                                     options=options,
                                     bounds=BOUNDS)

SAMPLE_IFS = SQUARE
TARGET_MARKOV = np.full((N_TRANSFORMS, N_TRANSFORMS), determinant_probabilities(SAMPLE_IFS))
target = iterate(markov_chooser(SAMPLE_IFS, TARGET_MARKOV), num_iters=1000)
render_points(target, show=True)

# Perform optimization
obj_func = get_obj_func(target, SAMPLE_IFS)
cost, winner = optimizer.optimize(obj_func, iters=100)
history = np.array(optimizer.pos_history)
"""print(history.shape)
differences = np.sum(np.abs(history - transforms_to_particle(SAMPLE_IFS)), axis=-1)
print(differences.shape)
plt.plot(differences)
plt.show()

transforms_frames = [render_transforms(particle_to_transforms(p)) for p in history]
render_gif(transforms_frames, show=True)
"""
chain = particle_to_markov(winner)
print(chain)
attractor = iterate(markov_chooser(SAMPLE_IFS, chain), num_iters=len(target))
render_points(attractor, show=True)
attractor = iterate(markov_chooser(SAMPLE_IFS, chain), num_iters=20000)
render_points(attractor, show=True)
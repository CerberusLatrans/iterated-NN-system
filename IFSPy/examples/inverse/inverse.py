import numpy as np
import pyswarms as psw
from optimize import get_bounds, get_dim, get_obj_func
from catalogue.leaves import FERN2D, SQUARE
from ifs import iterate
from optimize import particle_to_transforms
from visualize import render_transforms, render_points
from objective import hutchinson

# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
bounds = (np.array([-1,-1,-1,-1,-2,-2]),
          np.array([1,1,1,1,2,2]))

# Call instance of PSO
optimizer = psw.single.GlobalBestPSO(n_particles=20, dimensions=get_dim(), options=options, bounds=get_bounds())

target = iterate(SQUARE, num_iters=1000)
# Perform optimization
obj_func = get_obj_func(target)
cost, winner = optimizer.optimize(obj_func, iters=1)

ifs = particle_to_transforms(winner)
render_transforms(ifs, show=True)
collage = hutchinson(ifs, target)
render_points(collage, show=True)
attractor = iterate(ifs)
render_points(attractor, show=True)
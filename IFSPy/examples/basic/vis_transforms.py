import numpy as np

from visualize import render_transforms
from affine import Transformations
from catalogue.leaves import FERN2D
from catalogue.shapes import SQUARE

transforms = [Transformations.identity_affine,
              Transformations.translate(shift=(10, 10)),
              Transformations.reflect(axes=(True, True)),
              Transformations.rotate(degrees=np.pi/4),
              Transformations.scale(factor=(2,3)),
              Transformations.shear(factor=(5,4))]
#render_transforms(transforms, scale=0.1, show=True)
render_transforms(SQUARE,show=True)
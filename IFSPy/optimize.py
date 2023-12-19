import numpy as np
import pyswarms as psw
from pyswarms.utils.functions import single_obj

import numpy.typing as npt
from typing import Annotated, Callable, TypeVar

from objective import collage_loss
from affine import PointSet2D, Affine2D, apply_set, affine_norm


N = TypeVar("N") #N particles
D = TypeVar("D") #dimensions

#move to affine
def from_affine_dim(affine_dim: int = 2) -> int:
    return affine_dim**2 + affine_dim

#move to ifs
def get_dim(affine_dim: int = 2, num_codes: int = 4) -> int:
    return num_codes*(from_affine_dim(affine_dim))

def get_bounds(
        a_bounds: tuple[float, float] = (-1,1),
        b_bounds: tuple[float, float] = (-2,2), 
        affine_dim: int = 2,
        num_codes: int = 4
        ) -> tuple[npt.NDArray, npt.NDArray]:
    min_a, max_a = a_bounds
    min_b, max_b = b_bounds

    def compute_bound(a_bound: float, b_bound: float) -> npt.NDArray:
        return np.full((num_codes, from_affine_dim(affine_dim)), 
                       np.concatenate(
                        (np.full(affine_dim**2, a_bound),
                        np.full(affine_dim, b_bound)
                        ), axis=None))

    return (compute_bound(min_a, min_b).flatten(),
            compute_bound(max_a, max_b).flatten())

def particle_to_transforms(particle: npt.NDArray, dim: int = 2) -> list[Affine2D]:
    n_transforms = int(len(particle)/from_affine_dim(dim))
    transforms = np.reshape(particle, (n_transforms, dim, dim+1))
    return transforms + np.array([0, 0, 1])

def get_obj_func(target: PointSet2D, a1: float = 1, a2: float = 1) -> Callable:
    def obj_func(particles: Annotated[npt.NDArray, (N, D)]) -> Annotated[npt.NDArray, N]:
        return np.array([collage_loss(particle_to_transforms(p), target, a1=a1, a2=a2) for p in particles])
    
    return obj_func
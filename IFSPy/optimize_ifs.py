import numpy as np
import numpy.typing as npt
from typing import Annotated, Callable, TypeVar

from objective import collage_loss
from affine import apply_set, affine_norm
from ifs_typing import PointSet2D, Affine2D, Ifs2D

N = TypeVar("N") #N particles
D = TypeVar("D") #dimensions

#move to affine
def space_to_affine_dim(space_dim: int = 2) -> int:
    return space_dim**2 + space_dim

def get_bounds(
        a_bounds: tuple[float, float] = (-1,1),
        b_bounds: tuple[float, float] = (-2,2), 
        space_dim: int = 2,
        n_transforms: int = 4,
        reference: Ifs2D = None,
        ) -> tuple[npt.NDArray, npt.NDArray]:
    min_a, max_a = a_bounds
    min_b, max_b = b_bounds

    def compute_bound(a_bound: float, b_bound: float) -> npt.NDArray:
        return np.full((n_transforms, space_to_affine_dim(space_dim)), 
                       np.concatenate(
                        (np.full(space_dim**2, a_bound),
                        np.full(space_dim, b_bound)
                        ), axis=None))

    reference = transforms_to_particle(reference) if reference is not None else transforms_to_particle(np.identity(3))
    return (reference+compute_bound(min_a, min_b).flatten(),
            reference+compute_bound(max_a, max_b).flatten())

def particle_to_transforms(particle: npt.NDArray, dim: int = 2) -> list[Affine2D]:
    n_transforms = int(len(particle)/space_to_affine_dim(dim))
    transforms = np.reshape(particle, (n_transforms, dim, dim+1))
    return transforms + np.array([0, 0, 1])

def transforms_to_particle(transforms: Ifs2D) -> npt.NDArray:
    dim = transforms.shape[1] - 1
    particle = [t[:dim] for t in transforms]
    return np.array(particle).flatten()

def get_obj_func(target: PointSet2D, a1: float = 1, a2: float = 1) -> Callable:
    def obj_func(particles: Annotated[npt.NDArray, (N, D)]) -> Annotated[npt.NDArray, N]:
        return np.array([collage_loss(particle_to_transforms(p), target, a1=a1, a2=a2) for p in particles])
    
    return obj_func
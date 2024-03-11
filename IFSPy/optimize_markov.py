import numpy as np
import numpy.typing as npt
from typing import Annotated, Callable, TypeVar

from objective import chamfer_dist
from ifs_typing import PointSet2D, MarkovChain, Ifs2D
from ifs import iterate
from markov import markov_chooser, normalize_chain

N = TypeVar("N") #N particles
D = TypeVar("D") #dimensions

def get_bounds(
        bounds: tuple[float, float] = (0,1),
        n_transforms: int = 4
        ) -> tuple[npt.NDArray, npt.NDArray]:
    lower, upper = bounds
    return (np.full(n_transforms**2, lower), np.full(n_transforms**2, upper))

def particle_to_markov(particle: npt.NDArray) -> MarkovChain:
    return normalize_chain(np.reshape(particle, (n:=int(len(particle)**0.5), n)))

def markov_to_particle(chain: MarkovChain) -> npt.NDArray:
    return chain.flatten()

def get_obj_func(target: PointSet2D, ifs: Ifs2D) -> Callable:
    def predict(particle: npt.NDArray) -> PointSet2D:
        return iterate(
            markov_chooser(ifs, particle_to_markov(particle)),
            num_iters=len(target))
    def obj_func(particles: Annotated[npt.NDArray, (N, D)]) -> Annotated[npt.NDArray, N]:
        return np.array([chamfer_dist(predict(p), target) for p in particles])
    
    return obj_func
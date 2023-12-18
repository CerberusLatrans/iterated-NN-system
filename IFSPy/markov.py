import numpy as np
import numpy.typing as npt
from typing import TypeVar, Annotated

from ifs import Ifs2D, AffineGenerator

N = TypeVar("N")
MarkovChain = Annotated[npt.ArrayLike[npt.ArrayLike[np.float64]], (N,N)]

def get_probabilities(
        transforms: Ifs2D
        ) -> npt.ArrayLike[np.float64]:
    """Determines the affine selection probabilities corresponding to relative area (determinant)

    Args:
        transforms (list[Affine2D]): List of affine tranformations

    Returns:
        npt.NDArray[np.float64]: _description_
    """
    As = [np.array([t[0,:2], t[1,:2]]) for t in transforms]
    dets = [np.abs(np.linalg.det(t)) for t in As]
    return np.array(dets) / np.sum(dets)

def uniform_choice(
        transforms: Ifs2D
        ) -> AffineGenerator:
    """Selects a transform randomly

    Args:
        transforms (list[Affine2D]): _description_

    Returns:
        Affine2D: _description_
    """
    #while True: yield transforms[np.random.choice(len(transforms))]
    return markov_chooser(transforms, np.full((n:=len(transforms), n), 1/n))

def weighted_random_choice(
        transforms: Ifs2D, 
        weights: npt.ArrayLike[float] = None
        ) -> AffineGenerator:
    """Selects a transform randomly according to determinant weights

    Args:
        transforms (list[Affine2D]): _description_

    Returns:
        Affine2D: _description_
    """
    if not weights: weights = get_probabilities(transforms)
    #while True: yield transforms[np.random.choice(len(transforms), p=weights)]
    return markov_chooser(transforms, np.full((n:=len(transforms), n), weights))

def markov_chooser(
        transforms: Ifs2D,
        transition_matrix: MarkovChain
        ) -> AffineGenerator:
    state: int = np.random.choice(len(transition_matrix))
    while True:
        yield transforms[state:=np.random.choice(len(transforms),
                                                  p=transition_matrix[state])]
        
def markov_weighted_sum(
        chains: npt.ArrayLike[MarkovChain],
        weights: npt.ArrayLike[float] = None
        ) -> MarkovChain:
    if weights is None:
        weights = np.full(len(chains), 1/len(chains))
    normalized_weights = weights/np.sum(weights)
    return np.average(chains, weights=normalized_weights, axis=0)

def markov_interpolate(
        source: MarkovChain,
        target: MarkovChain,
        t: int=10
        ) -> npt.ArrayLike[MarkovChain]:
    #return [source + (target-source)*i/t for i in range(t)]
    return [markov_weighted_sum([source, target], [1-(i/t), i/t]) for i in range(t)]
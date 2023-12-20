import numpy as np
import numpy.typing as npt
from tqdm import tqdm
from typing import Generator

from ifs_typing import Ifs2D, AffineGenerator, MarkovChain

def determinant_probabilities(
        transforms: Ifs2D
        ) -> npt.NDArray[np.float64]:
    """Determines the affine selection probabilities corresponding to relative area (determinant)

    Args:
        transforms (list[Affine2D]): List of affine tranformations

    Returns:
        npt.NDArray[np.float64]: _description_
    """
    As = [np.array([t[0,:2], t[1,:2]]) for t in transforms]
    dets = [np.abs(np.linalg.det(t)) for t in As]
    return np.array(dets) / np.sum(dets)

def uniform_chooser(
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

def weighted_random_chooser(
        transforms: Ifs2D, 
        weights: npt.NDArray[np.float64] = None
        ) -> AffineGenerator:
    """Selects a transform randomly according to determinant weights

    Args:
        transforms (list[Affine2D]): _description_

    Returns:
        Affine2D: _description_
    """
    if not weights: weights = determinant_probabilities(transforms)
    #while True: yield transforms[np.random.choice(len(transforms), p=weights)]
    return markov_chooser(transforms, np.full((n:=len(transforms), n), weights))

def markov_indexer(
        transition_matrix: MarkovChain
        ) -> Generator[int, None, None]:
    state: int = np.random.choice(len(transition_matrix))
    while True:
        yield (state:=np.random.choice(len(transition_matrix), p=transition_matrix[state]))
    
def markov_chooser(
        transforms: Ifs2D,
        transition_matrix: MarkovChain
        ) -> AffineGenerator:
    indexer = markov_chooser(len(transforms), transition_matrix)
    while True:
        yield transforms[next(indexer)]
        
def markov_weighted_sum(
        chains: list[MarkovChain],
        weights: npt.NDArray[np.float64] = None
        ) -> MarkovChain:
    if weights is None:
        weights = np.full(len(chains), 1/len(chains))
    normalized_weights = weights/np.sum(weights)
    return np.average(chains, weights=normalized_weights, axis=0)

def markov_interpolate(
        source: MarkovChain,
        target: MarkovChain,
        t: int=10
        ) -> list[MarkovChain]:
    #return [source + (target-source)*i/t for i in range(t)]
    return [markov_weighted_sum([source, target], [1-(i/t), i/t]) for i in range(t)]

def markov_interpolation_series(
    chains: list[MarkovChain],
    t: int=10,
    ) -> list[MarkovChain]:
    chain_sequence = []
    for i in tqdm(range(len(chains)-1), desc="Interpolating..."):
        source, target = chains[i], chains[i+1]
        chain_sequence.extend(markov_interpolate(source, target, t=t))
    
    return chain_sequence
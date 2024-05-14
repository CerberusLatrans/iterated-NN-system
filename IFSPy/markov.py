import numpy as np
import numpy.typing as npt
from tqdm import tqdm
from typing import Generator

from ifs_typing import Ifs2D, AffineGenerator, MarkovChain

def normalize_chain(chain: MarkovChain) -> MarkovChain:
    """Normalizes a matrix such that each row sums to 1.

    Args:
        chain (MarkovChain): The unnormalized matrix.

    Returns:
        MarkovChain: The normalized matrix.
    """
    return chain/np.expand_dims(np.sum(chain, axis=-1), -1)

def determinant_probabilities(
        transforms: Ifs2D
        ) -> npt.NDArray[np.float64]:
    """Determines the selection probabilities determined by relative area (determinant).

    Args:
        transforms (Ifs2D): The set of affine transformations.

    Returns:
        npt.NDArray[np.float64]: The corresponding probabilities (sum to 1).
    """
    As = [np.array([t[0,:2], t[1,:2]]) for t in transforms]
    dets = [np.abs(np.linalg.det(t)) for t in As]
    return np.array(dets) / np.sum(dets)

def markov_indexer(
        transition_matrix: MarkovChain
        ) -> Generator[int, None, None]:
    """Samples from a number of states according to a markov chain.     

    Args:
        transition_matrix (MarkovChain): The markov chain matrix.

    Yields:
        Generator[int, None, None]: A generator yielding the next state (zero-indexed) of the markov step.
    """
    state: int = np.random.choice(len(transition_matrix))
    while True:
        yield (state:=np.random.choice(len(transition_matrix), p=transition_matrix[state]))
    
def markov_chooser(
        transforms: Ifs2D,
        transition_matrix: MarkovChain
        ) -> AffineGenerator:
    """Samples from the set of transforms according to a markov chain.

    Args:
        transforms (Ifs2D): The set of affine transformations.
        transition_matrix (MarkovChain): The markov chain matrix.

    Yields:
        Iterator[AffineGenerator]: A generator yielding the next transform of the markov step.
    """
    indexer = markov_indexer(transition_matrix)
    while True:
        yield transforms[next(indexer)]
        

def uniform_chooser(
        transforms: Ifs2D
        ) -> AffineGenerator:
    """Uniformly samples from the set of transforms.

    Args:
        transforms (Ifs2D): The set of affine transformations.

    Returns:
        AffineGenerator: A generator yielding the next transform sampled uniformly.
    """
    #while True: yield transforms[np.random.choice(len(transforms))]
    return markov_chooser(transforms, np.full((n:=len(transforms), n), 1/n))

def weighted_random_chooser(
        transforms: Ifs2D, 
        weights: npt.NDArray[np.float64] = None
        ) -> AffineGenerator:
    """Probabilistically samples from the set of transforms.

    Args:
        transforms (list[Affine2D]): The set of affine transformations.

    Returns:
        Affine2D: A generator yielding the next transform sampled probabilistically.
    """
    if weights is None: weights = determinant_probabilities(transforms)
    #while True: yield transforms[np.random.choice(len(transforms), p=weights)]
    return markov_chooser(transforms, np.full((n:=len(transforms), n), weights))

def markov_weighted_sum(
        chains: list[MarkovChain],
        weights: npt.NDArray[np.float64] = None
        ) -> MarkovChain:
    """Computes the linearly weighted sum across multiple transformation matrices.

    Args:
        chains (list[MarkovChain]): The set of equally sized transition matrices to combine.
        weights (npt.NDArray[np.float64], optional): Corresponding linear weights for each chain. Defaults to None.

    Returns:
        MarkovChain: The resulting linearly weighted markov chain transition matrix.
    """
    weights = weights if weights else np.full(len(chains), 1/len(chains))
    normalized_weights = weights/np.sum(weights)
    return np.average(chains, weights=normalized_weights, axis=0)

def markov_interpolate(
        source: MarkovChain,
        target: MarkovChain,
        t: int=10
        ) -> list[MarkovChain]:
    """Linearly interpolates between two markov transition matrices with t timeteps.
    TODO: implement beyond [0,1]

    Args:
        source (MarkovChain): The initial transition matrix.
        target (MarkovChain): The final transition matrix.
        t (int, optional): The number of steps between. Defaults to 10.

    Returns:
        list[MarkovChain]: A series of t interpolated transition matrices from source to target.
    """
    #return [source + (target-source)*i/t for i in range(t)]
    return [markov_weighted_sum([source, target], [1-(i/t), i/t]) for i in range(t)]

def markov_interpolation_series(
        chains: list[MarkovChain],
        t: int=10,
        ) -> list[MarkovChain]:
    """Linearly interpolates between n systems with t timesteps between each.

    Args:
        chains (list[MarkovChain]): The set of equally sized transition matrices to interpolate sequentially between.
        t (int, optional): The number of steps between each matrix. Defaults to 10.

    Returns:
        list[MarkovChain]: A series of n*t interpolated transition matrices from source to target.
    """
    chain_sequence = []
    for i in tqdm(range(len(chains)-1), desc="Interpolating..."):
        source, target = chains[i], chains[i+1]
        chain_sequence.extend(markov_interpolate(source, target, t=t))
    
    return chain_sequence
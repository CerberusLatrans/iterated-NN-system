import numpy as np
import numpy.typing as npt
from affine import Affine2D, Point2D, PointSet2D, apply, affine_interpolate, affine_weighted_sum
from typing import Generator, Callable
import itertools
import math
from tqdm import tqdm

def get_probabilities(transforms: list[Affine2D]) -> npt.NDArray[np.float64]:
    """Determines the affine selection probabilities corresponding to relative area (determinant)

    Args:
        transforms (list[Affine2D]): _description_

    Returns:
        npt.NDArray[np.float64]: _description_
    """
    As = [np.array([t[0,:2], t[1,:2]]) for t in transforms]
    dets = [np.abs(np.linalg.det(t)) for t in As]
    return np.array(dets) / np.sum(dets)

def random_choice(transforms: list[Affine2D]) -> Generator[Affine2D, None, None]:
    """Selects a transform randomly

    Args:
        transforms (list[Affine2D]): _description_

    Returns:
        Affine2D: _description_
    """
    while True: yield transforms[np.random.choice(len(transforms))]

def weighted_random_choice(transforms: list[Affine2D], weights: list[float] = None) -> Generator[Affine2D, None, None]:
    """Selects a transform randomly according to determinant weights

    Args:
        transforms (list[Affine2D]): _description_

    Returns:
        Affine2D: _description_
    """
    if not weights: weights = get_probabilities(transforms)
    while True: yield transforms[np.random.choice(len(transforms), p=weights)]

def markov_chooser(transforms: list[Affine2D], transition_matrix: list[list[float]]) -> Affine2D:
    state: int = np.random.choice(len(transition_matrix))

    while True:
        yield transforms[state:=np.random.choice(len(transforms), p=transition_matrix[state])]

def iterate(
    chooser: Generator[Affine2D, None, None]= weighted_random_choice, 
    max_iter: int=1000,
    origin: Point2D=np.array([0,0])
    ) -> PointSet2D:
    """Runs an IFS using the chooser to a number of iterations

    Args:
        chooser (Callable[[list[Affine2D]], Affine2D], optional): _description_. Defaults to weighted_random_choice.
        max_iter (int, optional): _description_. Defaults to 1000.
        origin (Point2D, optional): _description_. Defaults to np.array([0,0]).

    Returns:
        PointSet2D: _description_
    """
    points: list[Point2D] = [origin]
    for i in range(max_iter):
        points.append(apply(next(chooser),points[-1]))

    return np.array(points)

def ifs_weighted_sum(systems: list[list[Affine2D]], weights: list[float] = None) -> list[Affine2D]:
    """Computes the transformation-wise weighted sum of the IFS's

    Args:
        systems (list[list[Affine2D]]): _description_
        weights (list[float]): _description_
    """
    #MxNxAffine -> NxMxAffine
    if weights is None:
        weights = np.full(len(systems), 1/len(systems))
    systems_transform_wise = np.transpose(systems, (1,0,2,3))
   
    return [affine_weighted_sum(transform, weights) for transform in systems_transform_wise]
    

def closest_mapping(source_ifs: list[Affine2D], target_ifs: list[Affine2D]) -> list[int]:
    """_summary_

    Args:
        sources (list[Affine2D]): _description_
        targets (list[Affine2D]): _description_

    Returns:
        list[int]: _description_
    """
    perms = itertools.permutations(range(len(source_ifs)))
    smallest_diff = math.inf
    best_perm = None
    for p in perms:
        mapped_targets = [target_ifs[p[i]] for i in range(len(source_ifs))]
        diff = np.abs(np.subtract(source_ifs, mapped_targets)).sum()
        if diff < smallest_diff:
            smallest_diff = diff
            best_perm = p

    return best_perm

def ifs_interpolate(
        source_ifs: list[Affine2D], 
        target_ifs: list[Affine2D],
        mapping: list[int] = None,
        t: int=10) -> list[list[Affine2D]]:
    """Linearly interpolates between all of the sources and corresponding targets

    Args:
        sources (list[Affine2D]): _description_
        targets (list[Affine2D]): _description_
        mapping (list[int]): _description_
        t (int, optional): _description_. Defaults to 10.

    Returns:
        list[list[Affine2D]]: _description_
    """
    if mapping is None:
        mapping = closest_mapping(source_ifs, target_ifs)
    #NxTxAffine
    affine_interpolations = np.array(
        [affine_interpolate(source_ifs[i], target_ifs[mapping[i]], t) for i in range(len(target_ifs))])
    #TxNxAffine
    ifs_interpolations = affine_interpolations.transpose((1,0,2,3))
    return [[t for t in ifs] for ifs in ifs_interpolations]

def ifs_interpolate_series(
        systems: list[list[Affine2D]], 
        mappings: list[list[int]] = None,
        t: int = 10) -> list[list[Affine2D]]:
    ifs_sequence = []
    for i in tqdm(range(len(systems)-1), desc="Interpolating..."):
        source_ifs, target_ifs = systems[i], systems[i+1]
        mapping = None if mappings is None else mappings[i]
        ifs_sequence.extend(ifs_interpolate(source_ifs, target_ifs, mapping=mapping, t=t))
    
    return ifs_sequence
    





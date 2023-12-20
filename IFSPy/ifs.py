import numpy as np
import itertools
from tqdm import tqdm
import numpy.typing as npt
from typing import Generator

from affine import apply, affine_interpolate, affine_weighted_sum
from markov import weighted_random_chooser
from ifs_typing import Point2D, PointSet2D, Ifs2D, AffineGenerator

"""
A modules for iterating, combining, and interpolating between function systems.
"""

def iterate(
        chooser: AffineGenerator=weighted_random_chooser, 
        num_iters: int=10000,
        origin: Point2D=np.array([0,0]),
        ) -> PointSet2D:
    """Iteratively applies chosen affine transformations to the last point. Plays the Chaos Game.

    Args:
        chooser (AffineGenerator, optional): Generates the next transformation to apply. Defaults to weighted_random_chooser.
        num_iters (int, optional): The number of iterations to run. Defaults to 10000.
        origin (Point2D, optional): The starting point. Defaults to np.array([0,0]).

    Returns:
        PointSet2D: The resulting set of points after iterating.
    """
    points: PointSet2D = [origin]
    for i in range(num_iters):
        points.append(apply(next(chooser),points[-1]))

    return np.array(points)

def iterate_indexed(
        indexer: Generator[int, None, None],
        transforms: Ifs2D,
        num_iters: int=10000,
        origin: Point2D=np.array([0,0]),
        ) -> tuple[PointSet2D, list[int]]:
    """Version of `ifs.iterate` that also returns the transformation index of each choice.

    Args:
        indexer (Generator[int, None, None]): Generates the index of the next transformation to apply.
        transforms (Ifs2D): The transformations from which to pick.
        num_iters (int, optional): The number of iterations to run. Defaults to 10000.
        origin (Point2D, optional): The starting point. Defaults to np.array([0,0]).

    Returns:
        tuple[PointSet2D, list[int]]: The resulting set of points after iterating and the indices of the transformation choices.
    """
    points: PointSet2D = [origin]
    idxs = []
    for i in range(num_iters):
        points.append(apply(transforms[idx:=next(indexer)],points[-1]))
        idxs.append(idx)

    return np.array(points), idxs

def ifs_weighted_sum(
        systems: list[Ifs2D],
        weights: npt.NDArray[np.float64] = None
        ) -> Ifs2D:
    """ Computes the linearly weighted sum across multiple function systems.

    Args:
        systems (list[Ifs2D]): The set of equally sized systems to combine (by affine transformation).
        weights (npt.NDArray[np.float64], optional): Corresponding linear weights for each system. Defaults to None.

    Returns:
        Ifs2D: The resulting linearly weighted function system.
    """
    #MxNxAffine -> NxMxAffine
    if weights is None:
        weights = np.full(len(systems), 1/len(systems))
    systems_transform_wise = np.transpose(systems, (1,0,2,3))
   
    return [affine_weighted_sum(transform, weights) for transform in systems_transform_wise]

def ifs_interpolate(
        source_ifs: Ifs2D, 
        target_ifs: Ifs2D,
        mapping: npt.NDArray[np.int64] = None,
        t: int=10
        ) -> list[Ifs2D]:
    """Linearly interpolates between the two systems with t timeteps.

    Args:
        source_ifs (Ifs2D): The initial system.
        target_ifs (Ifs2D): The final system.
        mapping (npt.NDArray[np.int64], optional): A bijective mapping from the source to target system functions. Defaults to None (closest mapping).
        t (int, optional): The number of steps between. Defaults to 10.

    Returns:
        list[Ifs2D]: A series of t interpolated systems from source to target.
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
        systems: list[Ifs2D], 
        mappings: npt.NDArray[np.int64] = None,
        t: int = 10
        ) -> list[Ifs2D]:
    """Linearly interpolates between n systems with n*t total timeteps.

    Args:
        systems (list[Ifs2D]): The set of equally sized systems to interpolate sequentially between.
        mappings (npt.NDArray[np.int64], optional): A series of bijective mappings between the transformations of each pair of systems. Defaults to None (closest mappings).
        t (int, optional): The number of steps between each system. Defaults to 10.

    Returns:
        list[Ifs2D]: A series of n*t interpolated sequential systems.
    """
    ifs_sequence = []
    for i in tqdm(range(len(systems)-1), desc="Interpolating..."):
        source_ifs, target_ifs = systems[i], systems[i+1]
        mapping = None if mappings is None else mappings[i]
        ifs_sequence.extend(ifs_interpolate(source_ifs, target_ifs, mapping=mapping, t=t))
    
    return ifs_sequence
    
def closest_mapping(
        source_ifs: Ifs2D,
        target_ifs: Ifs2D
        ) -> npt.NDArray[np.int64]:
    """Computes the closest bijective transformation mapping between two systems by finding the minimum distance permutation.

    Args:
        source_ifs (Ifs2D): The system with "domain" functions.
        target_ifs (Ifs2D): The system with "range" functions.

    Returns:
        npt.NDArray[np.int64]: The closest (smallest matrix difference) computed mapping.
    """
    perms = itertools.permutations(range(len(source_ifs)))
    smallest_diff = np.inf
    best_perm = None
    for p in perms:
        mapped_targets = [target_ifs[p[i]] for i in range(len(source_ifs))]
        diff = np.abs(np.subtract(source_ifs, mapped_targets)).sum()
        if diff < smallest_diff:
            smallest_diff = diff
            best_perm = p

    return best_perm




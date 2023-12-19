import numpy as np
import itertools
from tqdm import tqdm
import numpy.typing as npt
from typing import Generator

from affine import apply, affine_interpolate, affine_weighted_sum
from markov import weighted_random_chooser
from ifs_typing import Point2D, PointSet2D, Ifs2D, AffineGenerator

def iterate(
        chooser: AffineGenerator=weighted_random_chooser, 
        max_iter: int=1000,
        origin: Point2D=np.array([0,0]),
        ) -> PointSet2D:
    """Runs an IFS using the chooser to a number of iterations

    Args:
        chooser (Callable[[list[Affine2D]], Affine2D], optional): _description_. Defaults to weighted_random_choice.
        max_iter (int, optional): _description_. Defaults to 1000.
        origin (Point2D, optional): _description_. Defaults to np.array([0,0]).

    Returns:
        PointSet2D: _description_
    """
    points: PointSet2D = [origin]
    for i in range(max_iter):
        points.append(apply(next(chooser),points[-1]))

    return np.array(points)

def iterate_indexed(
        indexer: Generator[int, None, None],
        transforms: Ifs2D,
        max_iter: int=1000,
        origin: Point2D=np.array([0,0]),
        ) -> tuple[PointSet2D, list[int]]:
    points: PointSet2D = [origin]
    idxs = []
    for i in range(max_iter):
        points.append(apply(transforms[idx:=next(indexer)],points[-1]))
        idxs.append(idx)

    return np.array(points), idxs

def ifs_weighted_sum(
        systems: list[Ifs2D],
        weights: npt.NDArray[np.float64] = None
        ) -> Ifs2D:
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

def ifs_interpolate(
        source_ifs: Ifs2D, 
        target_ifs: Ifs2D,
        mapping: npt.NDArray[np.int64] = None,
        t: int=10
        ) -> list[Ifs2D]:
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
        systems: list[Ifs2D], 
        mappings: npt.NDArray[np.int64] = None,
        t: int = 10
        ) -> list[Ifs2D]:
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
    """_summary_

    Args:
        sources (list[Affine2D]): _description_
        targets (list[Affine2D]): _description_

    Returns:
        list[int]: _description_
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




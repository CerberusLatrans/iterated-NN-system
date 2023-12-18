import numpy as np
import itertools
from tqdm import tqdm
from typing import Generator, Annotated, TypeVar
import numpy.typing as npt

from affine import Affine2D, Point2D, PointSet2D, apply, affine_interpolate, affine_weighted_sum
from markov import weighted_random_choice

N = TypeVar("N")
Ifs2D = Annotated[npt.ArrayLike[Affine2D], (N,3,3)]
AffineGenerator = Generator[Affine2D, None, None]

def iterate(
        chooser: AffineGenerator=weighted_random_choice, 
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

def ifs_weighted_sum(
        systems: npt.ArrayLike[Ifs2D],
        weights: npt.ArrayLike[float] = None
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
        mapping: npt.ArrayLike[int] = None,
        t: int=10
        ) -> npt.ArrayLike[Ifs2D]:
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
        systems: npt.ArrayLike[Ifs2D], 
        mappings: npt.ArrayLike[npt.ArrayLike[int]] = None,
        t: int = 10
        ) -> npt.ArrayLike[Ifs2D]:
    ifs_sequence = []
    for i in tqdm(range(len(systems)-1), desc="Interpolating..."):
        source_ifs, target_ifs = systems[i], systems[i+1]
        mapping = None if mappings is None else mappings[i]
        ifs_sequence.extend(ifs_interpolate(source_ifs, target_ifs, mapping=mapping, t=t))
    
    return ifs_sequence
    
def closest_mapping(
        source_ifs: Ifs2D,
        target_ifs: Ifs2D
        ) -> npt.ArrayLike[int]:
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




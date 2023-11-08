import numpy as np
import numpy.typing as npt
from affine import Affine2D, Point2D, PointSet2D, apply, affine_interpolate
from typing import Generator, Callable

def get_probabilities(transforms: list[Affine2D]) -> npt.NDArray[np.float64]:
    As = [np.array([t[0,:2], t[1,:2]]) for t in transforms]
    dets = [np.abs(np.linalg.det(t)) for t in As]
    return np.array(dets) / np.sum(dets)

def random_choice(transforms: list[Affine2D]) -> Affine2D:
    return transforms[np.random.choice(len(transforms))]

def weighted_random_choice(transforms: list[Affine2D]) -> Affine2D:
    weights = get_probabilities(transforms)
    return transforms[np.random.choice(len(transforms), p=weights)]

def iterate(
    transforms: list[Affine2D], 
    chooser: Callable[[list[Affine2D]], Affine2D]= weighted_random_choice, 
    max_iter: int=1000,
    origin: Point2D=np.array([0,0])
    ) -> PointSet2D:
    points: list[Point2D] = [origin]
    for i in range(max_iter):
        points.append(apply(chooser(transforms),points[-1]))

    return np.array(points)

def ifs_interpolate(
        source: list[Affine2D], 
        target: list[Affine2D],
        t: int=10) -> list[list[Affine2D]]:
    #NxTxAffine
    affine_interpolations = np.array([affine_interpolate(src, trg, t) for src,trg in zip(source, target)])
    #TxNxAffine
    ifs_interpolations = affine_interpolations.transpose((0,1,2))
    return [[t for t in ifs] for ifs in ifs_interpolations]

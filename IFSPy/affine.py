import numpy as np
from typing import Annotated, Generator, TypeVar
import numpy.typing as npt
import math

N = TypeVar("N")
Affine2D = Annotated[npt.NDArray[np.float64], (3,3)]
Point2D = Annotated[npt.NDArray[np.float64], (2,1)]
PointSet2D = Annotated[npt.NDArray[np.float64], (N, 2,1)]
Affine3D = Annotated[npt.NDArray[np.float64], (4,4)]
Point3D = Annotated[npt.NDArray[np.float64], (3,1)]
PointSet3D = Annotated[npt.NDArray[np.float64], (N, 3, 1)]

def apply(transform: Affine2D, point: Point2D) -> Point2D:
    """
    Applies the affine transformation to the given point
    """
    point = np.append(point, 1)
    return (transform@point)[:2]

def apply_set(transform: Affine2D, points: PointSet2D) -> PointSet2D:
    points = np.append(points, np.full((len(points),1),1), axis=-1)
    return (transform@points.T).T

def affine_morph(source: Affine2D, target: Affine2D) -> Affine2D:
    """
    Quaternions?
    """
    return np.linalg.solve(source,target)

def affine_interpolate(source: Affine2D, target: Affine2D, t: int=10) -> list[Affine2D]:
    """Linearly interpolates between the source an target with t timeteps

    Args:
        source (Affine2D): _description_
        target (Affine2D): _description_
        t (int, optional): _description_. Defaults to 10.

    Returns:
        list[Affine2D]: _description_
    """
    #return [source + (target-source)*i/t for i in range(t)]
    return [affine_weighted_sum([source, target], [1-(i/t), i/t]) for i in range(t)]

def affine_weighted_sum(transforms: list[Affine2D], weights: list[float] = None) -> Affine2D:
    """computes the weighted sum of the given transformation
    This is a generalization of affine.affine_interpolate

    Args:
        transforms (list[Affine2D]): _description_
        weights (list[float]): _description_

    Returns:
        Affine2D: _description_
    """
    if weights is None:
        weights = np.full(len(transforms), 1/len(transforms))
    normalized_weights = weights/np.sum(weights)
    return np.average(transforms, weights=normalized_weights, axis=0)

def affine_norm(t: Affine2D, ord: str = None) -> float:
    return np.linalg.norm(t[:-1, :-1], ord=ord)

def translate(t: Affine2D, shift: tuple[float, float] = (0, 0)) -> Affine2D:
    trans_mat = np.array([[1, 0, shift[0]],
                          [0, 1, shift[1]],
                          [0, 0 ,1]])
    return trans_mat@t

def reflect(t: Affine2D, axes: tuple[bool, bool] = (False, False)) -> Affine2D:
    trans_mat = np.array([[-1 if axes[0] else 1, 0, 0],
                          [0, -1 if axes[1] else 1, 0],
                          [0, 0 ,1]])
    return trans_mat@t

def scale(t: Affine2D, factor: tuple[float, float] = (1, 1)) -> Affine2D:
    scale_mat = np.array([[factor[0], 0, 0],
                          [0, factor[1], 0],
                          [0, 0 ,1]])
    return scale_mat@t

def rotate(t: Affine2D, degrees: float = 0) -> Affine2D:
    scale_mat = np.array([[math.cos(degrees), -math.sin(degrees), 0],
                          [math.sin(degrees), math.cos(degrees), 0],
                          [0, 0 ,1]])
    return scale_mat@t

def shear(t: Affine2D, factor: tuple[float, float] = (0, 0)) -> Affine2D:
    shear_mat = np.array([[1, factor[0], 0],
                          [factor[1], 1, 0],
                          [0, 0 ,1]])
    return shear_mat@t


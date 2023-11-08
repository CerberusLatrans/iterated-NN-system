import numpy as np
from typing import Annotated, Generator, TypeVar
import numpy.typing as npt 

N = TypeVar("N")
Affine2D = Annotated[npt.NDArray[np.float64], (3,3)]
Point2D = Annotated[npt.NDArray[np.float64], (2,1)]
PointSet2D = Annotated[npt.NDArray[np.float64], (N, 2,1)]
Affine3D = Annotated[npt.NDArray[np.float64], (4,4)]
Point3D = Annotated[npt.NDArray[np.float64], (3,1)]
PointSet3D = Annotated[npt.NDArray[np.float64], (N, 3, 1)]

def apply(transform: Affine2D, point: Point2D) -> Point2D:
    point = np.append(point, 1)
    return (transform@point)[:2]

def affine_morph(source: Affine2D, target: Affine2D) -> Affine2D:
    return np.linalg.solve(source,target)

def affine_interpolate(source: Affine2D, target: Affine2D, t: int=10) -> list[Affine2D]:
    return [source + (target-source)*i/t for i in range(t)]


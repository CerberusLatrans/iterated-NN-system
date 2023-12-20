import numpy as np
import numpy.typing as npt
from typing import Annotated, TypeVar, Generator

"""
A collection of custom IFSPy types.
"""

N = TypeVar("N")

Affine2D = Annotated[npt.NDArray[np.float64], (3,3)]
Point2D = Annotated[npt.NDArray[np.float64], (2,1)]
PointSet2D = Annotated[npt.NDArray[np.float64], (N,2,1)]

Ifs2D = Annotated[npt.NDArray[np.float64], (N,3,3)]
AffineGenerator = Generator[Affine2D, None, None]

MarkovChain = Annotated[npt.NDArray[np.float64], (N,N)]
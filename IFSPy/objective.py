import numpy as np
import numpy.typing as npt
from typing import TypeVar, Annotated

from affine import PointSet2D, apply_set, affine_norm
from ifs import Ifs2D

N = TypeVar("N")
M = TypeVar("M")

def cdist(
        x: Annotated[PointSet2D, N],
        y: Annotated[PointSet2D, M]
        ) -> Annotated[npt.NDArray[np.float64], (N,M)]:
    """
    Compute distance between each pair of the two collections of inputs.
    :param x: Nxd Tensor
    :param y: Mxd Tensor
    :res: NxM matrix where dist[i,j] is the norm between x[i,:] and y[j,:],
          i.e. dist[i,j] = ||x[i,:]-y[j,:]||

    """
    differences = np.expand_dims(x, 1) - np.expand_dims(y,0)
    """
    x: Nx1x3 Tensor
    [
        [[x1,x2,x3]]1
        ...
        [[x1,x2,x3]]N
    ]
    y: 1xMx3 Tensor
    [[
        [y1,y2,y3]1
        ...
        [y1,y2,y3]M
    ]]
    x-y: NxMx3 Tensor
    [
        [
            [x1-y1, x2-y2, x3-y3]1
            ...
            [x1-y1, x2-y2, x3-y3]M
        ]1
        ...
        [
            [x1-y1, x2-y2, x3-y3]1
            ...
            [x1-y1, x2-y2, x3-y3]M 
        ]N
    ]
    """
    distances = np.sqrt(np.sum(differences**2, -1))
    # NxM
    return distances

def chamfer_dist(
        pred: PointSet2D,
        target: PointSet2D
        ) -> float:
    dist_matrix = cdist(pred, target)

    # Modified Chamfer Loss (mean instead of sum, no squaring)
    #print(torch.min(dist_matrix, 1), torch.min(dist_matrix, 1)[0].size())
    #print(torch.min(dist_matrix, 0), torch.min(dist_matrix, 0)[0].size())
    #term_1 = torch.mean(torch.min(dist_matrix, 1)[0]) # N minimums
    #term_2 = torch.mean(torch.min(dist_matrix, 0)[0]) # M minimums

    #Modified Chamfer Loss (mean instead of sum-- invariant to number of points)
    term_1 = np.mean(np.square(np.min(dist_matrix, 1)))
    term_2 = np.mean(np.square(np.min(dist_matrix, 0)))
    res = term_1 + term_2
    return res

def hutchinson(
        transforms: Ifs2D,
        points: PointSet2D        
    ) -> PointSet2D:
    return np.concatenate([apply_set(t, points) for t in transforms])

def collage_loss(
        transforms: Ifs2D,
        target: PointSet2D,
        a1: float = 1,
        a2: float = 1
        ) -> float:
    chamfer_loss = chamfer_dist(hutchinson(transforms, target), target)  
    norms = np.array([affine_norm(t) for t in transforms])
    ms_norm = np.mean(np.square(norms))
    total_loss = a1*chamfer_loss + a2*ms_norm
    return total_loss
                 
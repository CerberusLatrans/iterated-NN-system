import numpy as np
import numpy.typing as npt
import torch
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
        target: PointSet2D,
        grad: bool = True,
        ) -> float:
    if grad:
        dists = ((pred.unsqueeze(0) - target.unsqueeze(1)) ** 2).sum(dim=2)
        mins_a = torch.min(dists, dim=0).values
        mins_b = torch.min(dists, dim=1).values
        return mins_a.mean() + mins_b.mean()
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
        points: PointSet2D,
        grad: bool = True,        
    ) -> PointSet2D:
    if grad:
        return torch.cat([apply_set(t, points, grad=True) for t in transforms])
    else:
        return np.concatenate([apply_set(t, points) for t in transforms])

def collage_loss(
        transforms: Ifs2D,
        target: PointSet2D,
        a1: float = 1,
        a2: float = 1,
        dist = chamfer_dist,
        grad: bool = True,
        decomp: bool = True,
        ) -> float:
    chamfer_loss = dist(hutchinson(transforms, target), target, grad=grad)  
    if grad:
        norms = torch.abs(torch.tensor([torch.norm(t[:-1, :-1]) for t in transforms]) - 0.5)
        ms_norm = torch.mean(torch.square(norms))
    else:
        norms = np.array([affine_norm(t) for t in transforms])
        ms_norm = np.mean(np.square(norms))
    total_loss = a1*chamfer_loss + a2*ms_norm
    if decomp:
        return total_loss, chamfer_loss, ms_norm
    else:
        return total_loss
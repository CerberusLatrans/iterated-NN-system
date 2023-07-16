import torch

def cdist(x, y):
    """
    Compute distance between each pair of the two collections of inputs.
    :param x: Nxd Tensor
    :param y: Mxd Tensor
    :res: NxM matrix where dist[i,j] is the norm between x[i,:] and y[j,:],
          i.e. dist[i,j] = ||x[i,:]-y[j,:]||

    """
    differences = x.unsqueeze(1) - y.unsqueeze(0)
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
    distances = torch.sum(differences**2, -1).sqrt()
    return distances

def chamfer_dist(pred, target):
    dist_matrix = cdist(pred, target)

    # Modified Chamfer Loss (mean instead of sum, no squaring)
    #print(torch.min(dist_matrix, 1), torch.min(dist_matrix, 1)[0].size())
    #print(torch.min(dist_matrix, 0), torch.min(dist_matrix, 0)[0].size())
    #term_1 = torch.mean(torch.min(dist_matrix, 1)[0]) # N minimums
    #term_2 = torch.mean(torch.min(dist_matrix, 0)[0]) # M minimums

    #Modified Chamfer Loss (mean instead of sum-- invariant to number of points)
    term_1 = torch.mean(torch.square(torch.min(dist_matrix, 1)[0]))
    term_2 = torch.mean(torch.square(torch.min(dist_matrix, 0)[0]))
    res = term_1 + term_2
    return res

def hutchinson_operator(
        points: torch.Tensor, # size nx3
        transforms: torch.Tensor, #size mx12
        ):
    points = torch.transpose(points,0, 1)
    def apply_transform(pts, t):
        A = torch.stack((t[0:3], t[3:6], t[6:9])) # 3x3
        b = t[9:12] #1x3
        return torch.add(torch.transpose(torch.matmul(A, pts), 0, 1), b)
    
    return torch.cat([apply_transform(points, t) for t in transforms])

def collage_loss(transforms, target, alpha=100, lam=1):
    chamfer_loss = chamfer_dist(hutchinson_operator(target, transforms), target)

    #penalize large eigenvalues magnitudes (close to 1) to enforce contractive transformations
    def get_eigvals(t):
        A = torch.stack((t[0:3], t[3:6], t[6:9])) # 3x3
        return torch.linalg.norm(torch.view_as_real(torch.linalg.eigvals(A)), dim=1)
    
    eigvals = torch.cat([get_eigvals(t) for t in transforms])
    #print(alpha*chamfer_loss)
    return alpha*chamfer_loss + lam*torch.sum(torch.square(eigvals))


#x = torch.Tensor([[1,2,3],[3,4,5]])
#y = torch.tensor([[0,5,5], [9,3,2], [0,1,1]])
#dist = chamfer_dist(x,y)
#print(dist)
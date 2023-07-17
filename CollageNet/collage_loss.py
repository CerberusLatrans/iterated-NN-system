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

"""
How diverse are the transformations in terms of x,y,z,translation?
What is the distance between all transformations?
"""
def transform_dists(transforms, dim=3):
    """
    Get p2 distances between all transformations (4 transforms = 6 dists between)
    By x,y,z,translation components separately
    Output: 4 x #dists Tensor
    """
    def format_components(t):
        """
        format the x,y,z,translation component vectors separately
        [x1, y1, z1, x2, y2, z2, x3, y3, z3, t1, t2, t3] ->
        [[x1, x2, x3]
        [y1, y2, y3]
        [z1, z2, z3]
        [t1, t2, t3]]
        """
        t = t.view(dim+1, dim)
        A = t[:dim]
        b = t[dim:]
        col_vecs = torch.cat((torch.transpose(A, 0, 1), b))
        return col_vecs
    
    vecs_by_transform = [format_components(t) for t in transforms]
    # group all x,y,z,translation components separately
    vecs_by_component = torch.stack(vecs_by_transform, dim=1)

    # all indices below the diagonal (non-redundant distance value indices)
    idxs = torch.transpose(torch.tril_indices(dim+1, dim+1, -1), 0, 1)
    # for n vectors, computes n(n-1)/2 p2 distances between them
    def compute_dists(vecs):
        dist_mat = torch.cdist(vecs, vecs)
        dists = torch.stack([dist_mat[i[0], i[1]] for i in idxs])
        return dists
    
    all_dists = torch.stack(
        [compute_dists(vecs_by_trnsfm) for vecs_by_trnsfm in vecs_by_component])
    
    return all_dists

def hutchinson_operator(
        points: torch.Tensor, # size nx3
        transforms: torch.Tensor, #size mx12
        ):
    points = torch.transpose(points,-1, -2)
    def apply_transform(pts, t):
        A = torch.stack((t[0:3], t[3:6], t[6:9])) # 3x3
        b = t[9:12] #1x3
        transformed = torch.add(torch.transpose(torch.matmul(A, pts), -1, -2), b)
        return transformed
    
    return torch.cat([apply_transform(points, t) for t in transforms])

def collage_loss(transforms, target, alpha=1, beta=1, theta=1):
    chamfer_loss = chamfer_dist(hutchinson_operator(target, transforms), target)

    #penalize large eigenvalues magnitudes (close to 1) to enforce contractive transformations
    def get_eigvals(t):
        A = torch.stack((t[0:3], t[3:6], t[6:9])) # 3x3
        return torch.linalg.norm(torch.view_as_real(torch.linalg.eigvals(A)), dim=1)
    
    eigvals = torch.cat([get_eigvals(t) for t in transforms])

    #penalize high transform redundancy (low component distance)
    avg_dist = torch.mean(transform_dists(transforms))

    print(chamfer_loss, avg_dist, torch.sum(torch.square(eigvals)))
    return alpha*chamfer_loss - beta*avg_dist+ theta*torch.mean(torch.square(eigvals))


#x = torch.Tensor([[1,2,3],[3,4,5]])
#y = torch.tensor([[0,5,5], [9,3,2], [0,1,1]])
#dist = chamfer_dist(x,y)
#print(dist)
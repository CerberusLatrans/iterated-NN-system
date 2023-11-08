import numpy as np
import torch
from collage_loss import hutchinson_operator, collage_loss
from visualize import rand_generate, plot_3d, get_probabilities
import plotly.graph_objects as go
from collagenet import CollageNet
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

fern_probs = np.array([0.01, 0.85, 0.07, 0.07])

fern_ifs = np.array([
    np.concatenate((
        [0.16, 0, 0],
        [0, 0.16, 0],
        [0, 0, 1],
        [0, 0, 0])),
    np.concatenate((
        [0.85, 0.04, 0.04],
        [-0.04, 0.85, 0.04],
        [0, 0, 1],
        [0, 1.60, 0])),
    np.concatenate((
        [0.20, -0.26, -0.26],
        [0.23, 0.22, -0.26],
        [0, 0, 1],
        [0, 1.60, 0])),
    np.concatenate((
        [-0.15, 0.28, 0.28],
        [0.26, 0.24, 0.28],
        [0, 0, 1],
        [0, 0.44, 0]))])
"""
fern_ifs = np.array([
    np.concatenate((
        [0, 0, 0],
        [0, 0.18, 0],
        [0, 0, 0],
        [0, 0, 0])),
    np.concatenate((
        [0.85, 0, 0],
        [0, 0.85, 0.1],
        [0, -0.1, 0.85],
        [0, 1.6, 0])),
    np.concatenate((
        [0.2, -0.2, 0],
        [0.2, 0.2, 0],
        [0, 0, 0.3],
        [0, 0.8, 0])),
    np.concatenate((
        [-0.2, 0.2, 0],
        [0.2, 0.2, 0],
        [0, 0, 0.3],
        [0, 0.8, 0]))])   
"""
if __name__ == "__main__":
    # test generation of fern via IFS
    fern = rand_generate(fern_ifs, fern_probs, max_iter=10000)
    #plot_3d(attractor)

    #test generaation of fern via collage
    #ifs = fern_ifs + np.random.rand(4,12)/100
    model = CollageNet(n_transforms=4, dim_latent=512)
    weights = "fern_trans=4_latent=512_A=1e-08_B=0_C=1_ep=200_n=10000_LR=3e-05"
    model.load_state_dict(torch.load("weights/{}".format(weights)))
    model.eval()
    ifs = model(torch.unsqueeze(torch.Tensor(fern), 0))
    print(ifs)
    collage = hutchinson_operator(torch.Tensor(fern), torch.Tensor(ifs))
    fern_t = np.transpose(fern)

    fig = plot_3d(collage)
    fig.add_trace(
        go.Scatter3d(
            x=fern_t[0],
            y=fern_t[1],
            z=fern_t[2],
            mode="markers",
            marker_color = "red",
            marker_size = 2,
        )
    )
    fig.show()

    print(collage_loss(torch.Tensor(ifs), torch.Tensor(fern)))

    probs = get_probabilities(ifs)
    ifs_attractor = rand_generate(ifs, probs, max_iter=10000)
    print(probs)
    fig = plot_3d(ifs_attractor)
    fig.add_trace(
        go.Scatter3d(
            x=fern_t[0],
            y=fern_t[1],
            z=fern_t[2],
            mode="markers",
            marker_color = "red",
            marker_size = 2,
        )
    )
    fig.show()


"""
Strategies
1. Optimize Chamfer -> Optimize Diversity and Eigen
`

First transform is throwing everything else off
need to coerce to contract more (reference page 74 and 75)
Contraction: rewards elongating along line (FIX)
IDEA: all x,y,z vectors need to have magnitude <1?
Follow transforms need to prioritize chamfer first 
(fill in rest of the target accurately)

Discarding translation Diversity Reward

Change network architecture to combine local and global features?

If Chamfer and Contraction are good enough, diversity reward should be unnecessary

Generative Idea: For N objects, create an N vertex polygon
Every point within the polygon is an IFS, with vertex points being the original objects
"""
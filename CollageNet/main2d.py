import numpy as np
import torch
from collage_loss import hutchinson_operator, collage_loss
from visualize import rand_generate, plot_2d, get_probabilities, plot_2d_pil
import plotly.graph_objects as go
from collagenet import CollageNet

fern_probs = np.array([0.01, 0.85, 0.07, 0.07])

fern_ifs = np.array([
    np.concatenate((
        [0.16, 0],
        [0, 0.16],
        [0, 0])),
    np.concatenate((
        [0.85, 0.04],
        [-0.04, 0.85],
        [0, 1.60])),
    np.concatenate((
        [0.20, -0.26],
        [0.23, 0.22],
        [0, 1.60])),
    np.concatenate((
        [-0.15, 0.28],
        [0.26, 0.24],
        [0, 0.44]))])

if __name__ == "__main__":
    # test generation of fern via IFS
    fern = rand_generate(fern_ifs, fern_probs, max_iter=10000, dim=2)
    #plot_3d(attractor)

    #test generaation of fern via collage
    MODEL = False
    if MODEL:
        model = CollageNet(n_transforms=4, dim_latent=512, dim_space=2)
        weights = "fern2d_trans=4_latent=512_A=1_B=0_C=1_ep=1000_n=10000_LR=3e-05"
        model.load_state_dict(torch.load("weights/{}".format(weights)))
        model.eval()
        ifs = model(torch.unsqueeze(torch.Tensor(fern), 0))
    else:
        ifs = fern_ifs# + np.random.rand(4,6)/60
    
    print(ifs)
    collage = hutchinson_operator(torch.Tensor(fern), torch.Tensor(ifs), dim=2)
    plot_2d_pil(fern, (200,200))
    #plot_2d_pil(collage, (100,100))
    fern_t = np.transpose(fern)

    """
    fig = plot_2d(collage)
    fig.add_trace(
        go.Scatter(
            x=fern_t[0],
            y=fern_t[1],
            mode="markers",
            marker_color = "red",
            marker_size = 2,
        )
    )
    fig.update_xaxes(range=[-10, 10])
    fig.update_yaxes(range=[0, 20])
    fig.show()

    print(collage_loss(torch.Tensor(ifs), torch.Tensor(fern), dim=2, breakdown=True))

    probs = get_probabilities(ifs, dim=2)
    ifs_attractor = rand_generate(ifs, probs, max_iter=10000, dim=2)
    print(probs)
    fig = plot_2d(ifs_attractor)
    fig.add_trace(
        go.Scatter(
            x=fern_t[0],
            y=fern_t[1],
            mode="markers",
            marker_color = "red",
            marker_size = 1,
        )
    )
    
    fig.update_xaxes(range=[-10, 10])
    fig.update_yaxes(range=[0, 20])
    fig.show()"""

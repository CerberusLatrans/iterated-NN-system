import numpy as np
import torch
from collage_loss import hutchinson_operator, collage_loss
from visualize import rand_generate, plot_3d
import plotly.graph_objects as go

fern_probs = np.array([0.01, 0.85, 0.07, 0.07])
fern_ifs = np.array([
    np.concatenate((
        [0, 0, 0],
        [0, 0.16, 0],
        [0, 0, 0.16],
        [0, 0, 0])),
    np.concatenate((
        [0.85, 0.04, 0.04],
        [-0.04, 0.85, 0.04],
        [-0.04, -0.04, 0.85],
        [0, 1.60, 0])),
    np.concatenate((
        [0.20, -0.26, -0.26],
        [0.23, 0.22, -0.26],
        [0.23, 0.23, 0.24],
        [0, 1.60, 0])),
    np.concatenate((
        [-0.15, 0.28, 0.28],
        [0.26, 0.24, 0.28],
        [0.26, 0.26, 0.39],
        [0, 0.44, 0]))])   


# test generation of fern via IFS
attractor = rand_generate(fern_ifs, fern_probs)
attractor2 = rand_generate(fern_ifs, fern_probs)
#plot_3d(attractor)

#test generaation of fern via collage
collage = hutchinson_operator(torch.Tensor(attractor), torch.Tensor(fern_ifs))
print(collage.size())
print(attractor.shape)
fig = plot_3d(collage)
attractor_t = np.transpose(attractor)
fig.add_trace(
    go.Scatter3d(
        x=attractor_t[0],
        y=attractor_t[1],
        z=attractor_t[2],
        mode="markers",
        marker_color = "red",
        marker_size = 2,
    )
)
fig.show()

print(collage_loss(torch.Tensor(fern_ifs), torch.Tensor(attractor)))
import numpy as np
import torch
from collage_loss import hutchinson_operator, collage_loss
from visualize import rand_generate, plot_3d, get_probabilities
import plotly.graph_objects as go
from collagenet import CollageNet

fern_probs = np.array([0.01, 0.85, 0.07, 0.07])
fern_ifs = np.array([
    np.concatenate((
        [0.16, 0, 0],
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
fern = rand_generate(fern_ifs, fern_probs, max_iter=10000)
#plot_3d(attractor)

#test generaation of fern via collage
#ifs = fern_ifs + np.random.rand(4,12)/100
model = CollageNet(n_transforms=4)
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

ifs_attractor = rand_generate(ifs, get_probabilities(ifs), max_iter=10000)
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
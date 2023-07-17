import torch
import numpy as np
import matplotlib.pyplot as plt
from collagenet import CollageNet
from collage_loss import collage_loss
from visualize import rand_generate
from main import fern_ifs, fern_probs

"""
HYPERPARAMETERS
=================
"""
N_TRANSFORMS = 4
DIM_LATENT = 512

model = CollageNet(n_transforms=N_TRANSFORMS, dim_latent=DIM_LATENT)
loss_function = collage_loss
ALPHA = 1
BETA = 1
THETA = 1

LR = 3e-3
weight_decay = 1e-8
optimizer = torch.optim.Adam(model.parameters(), lr = LR, weight_decay = weight_decay)

EPOCHS = 100
N_POINTS = 100000
ground = torch.unsqueeze(torch.Tensor(rand_generate(fern_ifs, fern_probs, max_iter=N_POINTS)), dim=0)
SAVE = True
PATH = "weights/fern_trans={}_latent={}_A={}_B={}_C={}_ep={}_n={}_LR={}"\
.format(N_TRANSFORMS, DIM_LATENT, ALPHA, BETA, THETA, EPOCHS, N_POINTS, LR)
"""
=================
"""

if __name__ == "__main__":
    outputs = []
    losses = []
    for epoch in range(EPOCHS):
        pred = model(ground)
        loss = loss_function(pred, ground, alpha=ALPHA, beta=BETA, theta=THETA)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        if epoch%1==0:
            pass
            #print(losses[-1])

    if SAVE:
        torch.save(model.state_dict(), PATH)
    plt.plot(losses)
    plt.show()
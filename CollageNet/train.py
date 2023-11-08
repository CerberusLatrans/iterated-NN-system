import torch
import numpy as np
import matplotlib.pyplot as plt
from collagenet import CollageNet
from collage_loss import collage_loss
from visualize import rand_generate
from main import fern_ifs, fern_probs
from main2d import fern_ifs

"""
HYPERPARAMETERS
=================
"""
DIM_SPACE = 2
N_TRANSFORMS = 4
DIM_LATENT = 512

model = CollageNet(n_transforms=N_TRANSFORMS, dim_space=DIM_SPACE, dim_latent=DIM_LATENT)
loss_function = collage_loss
ALPHA = 0
BETA = 0
THETA = 1

LR = 3e-3
weight_decay = 1e-8
optimizer = torch.optim.Adam(model.parameters(), lr = LR, weight_decay = weight_decay)

EPOCHS = 1000
N_POINTS = 10000
ground = torch.unsqueeze(torch.Tensor(rand_generate(fern_ifs, fern_probs, max_iter=N_POINTS, dim=DIM_SPACE)), dim=0)
SAVE = True
PATH = "weights/fern{}d_trans={}_latent={}_A={}_B={}_C={}_ep={}_n={}_LR={}"\
.format(DIM_SPACE, N_TRANSFORMS, DIM_LATENT, ALPHA, BETA, THETA, EPOCHS, N_POINTS, LR)
"""
=================
"""

if __name__ == "__main__":
    losses = []
    chamfers = []
    distances = []
    contractions = []
    for epoch in range(EPOCHS):
        pred = model(ground)
        loss, chamfer, dist, contract = loss_function(
            pred, ground, alpha=ALPHA, beta=BETA, theta=THETA, breakdown=True, dim=DIM_SPACE)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        chamfers.append(chamfer.item())
        distances.append(0)#dist.item())
        contractions.append(contract.item())
        if epoch%10==0:
            print("ITER {} LOSS: {} : Chamfer {} | AvgDist {} | Contr {}".format(
                epoch, losses[-1],chamfers[-1], distances[-1], contractions[-1]))

    if SAVE:
        torch.save(model.state_dict(), PATH)
    print(PATH)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    #plt.plot(losses)
    ax1.plot(chamfers)
    #plt.plot(distances)
    ax2.plot(contractions)
    plt.show()

"""
observations:
contraction can be lowered effectively with higher learning rate
have two separate optimizers?
use last avg contraction value as contraction learning rate?
"""
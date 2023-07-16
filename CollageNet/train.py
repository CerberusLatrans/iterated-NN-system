import torch
import numpy as np
import matplotlib.pyplot as plt
from collagenet import CollageNet
from collage_loss import collage_loss
from visualize import rand_generate

"""
HYPERPARAMETERS
=================
"""
model = CollageNet()
ground = fern
loss_function = collage_loss
LR = 3e-5
weight_decay = 1e-8
optimizer = torch.optim.Adam(model.parameters(), lr = LR, weight_decay = weight_decay)
EPOCHS = 1000
N_POINTS = 1000

SAVE = True
PATH = "weights/hidden=32_epoch=1000_n=1000"
"""
=================
"""

    
if __name__ == "__main__":
    outputs = []
    losses = []
    for epoch in range(EPOCHS):
        pred = torch.tensor(transform_to_points(model, n=N_POINTS), requires_grad=True)
        target = torch.tensor(transform_to_points(ground, n=N_POINTS), requires_grad=True)
        loss = loss_function(pred, target)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        if epoch%100==0:
            print(losses[-1])

    if SAVE:
        torch.save(model.state_dict(), PATH)
    plt.plot(losses)
    plt.show()

    fig, axs = plt.subplots(2, 3)
    xs = np.linspace(0,1,100).astype(np.float32)
    xs_tensor = torch.unsqueeze(torch.from_numpy(xs),1)
    model_out = np.transpose(model(xs_tensor).detach().numpy())
    fern_out = np.transpose(np.array([fern(x) for x in xs]))
    for i,ax in enumerate(axs.ravel()):
        ax.plot(xs, model_out[i])
        ax.plot(xs, fern_out[i])

    plt.show()
import torch
import matplotlib.pyplot as plt
import numpy as np
from random import random

class IterNet2D(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.layers = torch.nn.Sequential(
            torch.nn.Linear(1, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 6)
        )
        self.wide = torch.nn.Sequential(
            torch.nn.Linear(1, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 6)
        )
        self.long = torch.nn.Sequential(
            torch.nn.Linear(1, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 16),
            torch.nn.ReLU(),
            torch.nn.Linear(16, 6)
        ) 
    
    # (random) number (seed) input
    def forward(self, x):
        """
        Affine transformation (6d) output
        [[a, b]     [[e],
         [c, d]] +   [f]]
        """
        out = self.long(x)
        return out

def fern(r):
    if r < 0.01:
        return torch.tensor([0, 0, 0, 0.16, 0, 0])
    elif r < 0.86:
        return torch.tensor([0.85, 0.04, -0.04, 0.85, 0, 1.60])
    elif r < 0.93:
        return torch.tensor([0.20, -0.26, 0.23, 0.22, 0, 1.60])
    else:
        return torch.tensor([-0.15, 0.28, 0.26, 0.24, 0, 0.44])

if __name__ == "__main__":
    """
    HYPERPARAMETERS
    =================
    """
    model = IterNet2D()
    loss_function = torch.nn.MSELoss()
    LR = 1e-5
    weight_decay = 1e-8
    EPOCHS = 10
    SAMPLES = 10000

    SAVE = False
    PATH = "weights"
    """
    =================
    """

    optimizer = torch.optim.Adam(model.parameters(), lr = LR, weight_decay = weight_decay)

    outputs = []
    losses = []
    for epoch in range(EPOCHS):
        for i in range(SAMPLES):
            r = torch.tensor([random()])
            pred = model(r)
            ground = fern(r)
            loss = loss_function(pred, ground)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if i%10==0:
                losses.append(loss.item())
        print(losses[-1])

    if SAVE:
        torch.save(model.state_dict(), PATH)
    plt.plot(losses)
    plt.show()

    fig, axs = plt.subplots(2, 3)
    xs = np.linspace(0,1,100).astype(np.float32)
    xs_tensor = torch.unsqueeze(torch.from_numpy(xs),1)
    model_out = np.transpose(model(xs_tensor).detach().numpy())
    fern_out = np.transpose(np.array([fern(x).detach().numpy() for x in xs]))
    for i,ax in enumerate(axs.ravel()):
        ax.plot(xs, model_out[i])
        ax.plot(xs, fern_out[i])

    plt.show()
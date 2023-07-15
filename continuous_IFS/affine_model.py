import torch
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import directed_hausdorff

class IterNet2D(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.layers = torch.nn.Sequential(
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
        self.short = torch.nn.Sequential(
            torch.nn.Linear(1, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 6)
        ) 
    
    # (random) number (seed) input
    def forward(self, x):
        """
        Affine transformation (6d) output
        [[a, b]     [[e],
         [c, d]] +   [f]]
        """
        out = self.short(x)
        return out

def fern(r):
    if r < 0.01:
        return [0, 0, 0, 0.16, 0, 0]
    elif r < 0.86:
        return [0.85, 0.04, -0.04, 0.85, 0, 1.60]
    elif r < 0.93:
        return [0.20, -0.26, 0.23, 0.22, 0, 1.60]
    else:
        return [-0.15, 0.28, 0.26, 0.24, 0, 0.44]

if __name__ == "__main__":
    """
    HYPERPARAMETERS
    =================
    """
    model = IterNet2D()
    loss_function = torch.nn.MSELoss()
    LR = 3e-4
    weight_decay = 1e-8
    SAMPLES = 10000
    N_POINTS = 100

    SAVE = True
    PATH = "weights/batch100"
    """
    =================
    """

    optimizer = torch.optim.Adam(model.parameters(), lr = LR, weight_decay = weight_decay)

    outputs = []
    losses = []
    for sample in range(SAMPLES):
        r = torch.tensor(np.random.rand(N_POINTS, 1).astype(np.float32))
        pred = model(r)
        ground = torch.tensor([fern(x.item()) for x in r])

        loss = loss_function(pred, ground)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        if sample%100==0:
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
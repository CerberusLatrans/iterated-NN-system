import torch

class CollageNet(torch.nn.Module):
    def __init__(self, n_transforms, dim_space=3, dim_latent=256):
        super().__init__()

        self.n_transforms = n_transforms
        self.dim_space = dim_space
        self.n_affine = self.dim_space**2 + self.dim_space
        self.dim_latent = dim_latent

        self.encode = torch.nn.Sequential(
            torch.nn.Conv1d(self.dim_space, int(self.dim_latent/4), 1),
            torch.nn.ReLU(),
            torch.nn.Conv1d(int(self.dim_latent/4), int(self.dim_latent/2), 1),
            torch.nn.ReLU(),
            torch.nn.Conv1d(int(self.dim_latent/2), self.dim_latent, 1),
            torch.nn.ReLU(),
        )
        self.pred_affine = torch.nn.Sequential(
            torch.nn.Linear(self.dim_latent, int(self.dim_latent/2)),
            torch.nn.ReLU(),
            torch.nn.Linear(int(self.dim_latent/2), int(self.dim_latent/4)),
            torch.nn.ReLU(),
            torch.nn.Linear(int(self.dim_latent/4), self.n_affine*self.n_transforms),
        ) 
    
    # (random) number (seed) input
    def forward(self, x):
        x = torch.transpose(x, 1, 2)
        x = self.encode(x)
        #print(x.size())
        x = torch.max(x, 2, keepdim=False)[0]
        #print(x.size())
        x = self.pred_affine(x)
        #print(x.size())
        x = x.view(self.n_transforms, self.n_affine)
        #print(x.size())
        return x
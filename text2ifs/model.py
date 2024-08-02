import torch

class IFSNet(torch.nn.Module):
    def __init__(self, arity, embedding_space=512):
        super().__init__()

        self.arity = arity
        self.embedding_space = embedding_space

        self.pred_ifs = torch.nn.Sequential(
            torch.nn.Linear(self.embedding_space, int(self.embedding_space/2)), #256
            torch.nn.ReLU(),
            torch.nn.Linear(int(self.embedding_space/2), int(self.embedding_space/4)), #128
            torch.nn.ReLU(),
            torch.nn.Linear(int(self.embedding_space/4), self.arity*12),
            torch.nn.Tanh(),
        ) 
    
    def forward(self, x):
        x = self.pred_ifs(x)
        return x
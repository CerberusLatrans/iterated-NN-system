import torch
import numpy as np
import matplotlib.pyplot as plt
from model import IFSNet
from dataset import IFSDataset
from torch.utils.data import Dataset, DataLoader

"""
HYPERPARAMETERS
=================
"""
ARITY = 4
EMBEDDING_DIM = 512

model = IFSNet(arity=ARITY, embedding_space=EMBEDDING_DIM)
loss_function = torch.nn.MSELoss()

LR = 1e-3
weight_decay = 1e-8
optimizer = torch.optim.Adam(model.parameters(), lr = LR, weight_decay = weight_decay)

EPOCHS = 100
SAVE = True

"""
DATALOADER
=================
"""
ANNOTATION_FILE = "test_annotations.csv"
JSON_DIR = "ifs_data"
EMBEDDING_MODEL = "t5-small"
SCRAMBLE_IFS = True
train_dataset = IFSDataset(arity=ARITY,
                           scramble_ifs=SCRAMBLE_IFS,
                           annotations_file=ANNOTATION_FILE,
                           embedding_model=EMBEDDING_MODEL,
                           json_dir=JSON_DIR)
BATCH_SIZE = len(train_dataset)
train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE)

PATH = "weights/arity={}_ep={}_LR={}_nsamples={}"\
.format(ARITY, EPOCHS, LR, len(train_dataset))

if __name__ == "__main__":
    losses = []
    model.train()
    for epoch in range(EPOCHS):
        for batch, (X, y) in enumerate(train_dataloader):
            pred = model(X)
            loss = loss_function(pred, y)
            
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            losses.append(loss.item())

    if SAVE:
        torch.save(model.state_dict(), PATH)
    print(PATH)

    fig, ax1 = plt.subplots()
    plt.plot(losses)
    plt.show()

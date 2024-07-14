from transformers import T5EncoderModel, T5Tokenizer 
import os
import json
import torch
import torch.nn as nn
from torch.nn import functional as F
import pandas as pd
from torch.utils.data import Dataset
import numpy as np

class IFSDataset(Dataset):
    def __init__(self,
                 arity,
                 annotations_file,
                 json_dir,
                 embedding_model,
                 scramble_ifs=True,
                 ifs_noise_factor=1,
                 text_noise_factor=1):
        self.arity = arity
        self.annotations = pd.read_csv(annotations_file)
        self.json_dir = json_dir
        self.ifs_noise_factor = ifs_noise_factor
        self.text_noise_factor = text_noise_factor
        self.scramble_ifs = scramble_ifs

        self.tok = T5Tokenizer.from_pretrained(embedding_model)
        self.enc = T5EncoderModel.from_pretrained(embedding_model)

        # initialize dataframe with read json and read ifs
        self.df = self.annotations
        self.df["embeddings"] = self.df["desc"].apply(self._encode_text)
        self.df["ifs"] = self.df["file"].apply(self._fetch_ifs)

        #print(self.df.to_string())
    
    def __len__(self):
        return len(self.annotations)#*self.ifs_noise_factor*self.text_noise_factor
    
    def __getitem__(self, index):
        row = self.df.iloc[index]
        return torch.tensor(row['embeddings']).float(), torch.tensor(row['ifs']).float()

    def _fetch_ifs(self, filename):
        fp = os.path.join(self.json_dir, filename)
        with open(fp, mode="r") as f:
            ifs_json = json.load(f)
            ifs_mat = [list(affine.values()) for affine in ifs_json.values()]

        id = [1,0,0,0,
              0,1,0,0,
              0,0,1,0]
        if len(ifs_mat)>self.arity:
            ifs_mat = ifs_mat[:self.arity]
        elif len(ifs_mat)<self.arity:
            for _ in range(self.arity-len(ifs_mat)):
                ifs_mat.append(id)

        if self.scramble_ifs:
            return np.random.permutation(np.array(ifs_mat)).flatten()
        else:
            return np.array(ifs_mat).flatten()

    def _encode_text(self, text):
        tokenized = self.tok(text, return_tensors="pt")
        output = self.enc.encoder(
            input_ids=tokenized["input_ids"], 
            attention_mask=tokenized["attention_mask"], 
            return_dict=True
        )
        emb = output.last_hidden_state
        avg_emb = emb.mean(dim=1).detach().numpy().flatten()
        return avg_emb
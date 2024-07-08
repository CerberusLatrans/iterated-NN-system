import torch
from model import IFSNet

ARITY = 4
AFFINE_LEN = 12
EMB_DIM = 512
weight_path = "weights/arity=4_ep=100_LR=0.001"
def main():
    torch_model = IFSNet(arity=4)
    torch_model.load_state_dict(torch.load(weight_path))
    torch_model.eval()
    dummy_input = torch.zeros(EMB_DIM)
    torch.onnx.export(torch_model, dummy_input, 'ifsnet.onnx', verbose=True)

if __name__ == '__main__':
    main()
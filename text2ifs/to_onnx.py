import torch
from model import IFSNet

ARITY = 4
AFFINE_LEN = 12
EMB_DIM = 512
weight_folder = "weights"
weight_path = "arity=4_ep=100_LR=0.001_nsamples=3"
web_app_model_path = "../ifs-web-app/static/models/"

model_name = "IFSNET_"+weight_path+".onnx"
def main():
    torch_model = IFSNet(arity=4)
    torch_model.load_state_dict(torch.load(weight_folder+"/"+weight_path))
    torch_model.eval()
    dummy_input = torch.zeros(EMB_DIM)
    torch.onnx.export(torch_model, dummy_input, web_app_model_path+model_name, verbose=True)

if __name__ == '__main__':
    main()
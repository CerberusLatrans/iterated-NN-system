import onnx.parser
from onnx import helper, shape_inference, load

path = "./t5_encoder_model.onnx"
#path = "./text2ifs/ifsnet.onnx"
model = load(path)
print(model.graph.input)
"""inferred_model = shape_inference.infer_shapes(model)

with open("log.txt", "w") as f:
    f.write(str(inferred_model))"""
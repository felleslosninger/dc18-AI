import cntk as C
z = C.Function.load("models/model.onnx", format=C.ModelFormat.ONNX)

# TODO: do some neural network magicking

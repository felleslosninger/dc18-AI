import cntk as C

z = C.Function.load("../models/big_model.onnx", format=C.ModelFormat.ONNX)

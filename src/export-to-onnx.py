from model_converters import KerasToTensorflow
from onnx_tf.frontend import tensorflow_graph_to_onnx_model

# convert Keras .h5 (HDF5) format to TensorFlow frozen .pb format
KerasToTensorflow.convert("model.h5", "export")

# convert Tensorflow frozen .pb format to ONNX format
with tf.gfile.GFile("export/model.pb", "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    onnx_model = tensorflow_graph_to_onnx_model(graph_def,
                                     "fc2/add",
                                     opset=6)

    file = open("export/model.onnx", "wb")
    file.write(onnx_model.SerializeToString())
    file.close()

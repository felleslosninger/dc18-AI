import tensorflow as tf
from tensorflow.python.util import compat
from tensorflow.core.protobuf import saved_model_pb2

from model_converters import KerasToTensorflow
from onnx_tf.frontend import tensorflow_graph_to_onnx_model

# convert Keras .h5 (HDF5) format to TensorFlow frozen .pb format
KerasToTensorflow.convert("model.h5", "export")

# convert Tensorflow frozen .pb format to ONNX format
with tf.gfile.GFile("export/saved_model.pb", "rb") as f:
    data = compat.as_bytes(f.read());
    sm = saved_model_pb2.SavedModel();
    sm.ParseFromString(data);
    
    graph_def = sm.meta_graphs[0].graph_def;
    onnx_model = tensorflow_graph_to_onnx_model(graph_def,
                                     "dense_1/Softmax",
                                     opset=6)

    file = open("export/model.onnx", "wb")
    file.write(onnx_model.SerializeToString())
    file.close()

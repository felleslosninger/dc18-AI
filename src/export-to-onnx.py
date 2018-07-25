import tensorflow as tf
from tensorflow.python.util import compat
from tensorflow.core.protobuf import saved_model_pb2

#from model_converters import KerasToTensorflow
from onnx_tf.frontend import tensorflow_graph_to_onnx_model

import os

# convert Tensorflow frozen .pb format to ONNX format
with tf.gfile.GFile("models/model.pb", "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    onnx_model = tensorflow_graph_to_onnx_model(graph_def,
                                     "outputs",
                                     opset=6)

    file = open("models/model.onnx", "wb")
    file.write(onnx_model.SerializeToString())
    file.close()

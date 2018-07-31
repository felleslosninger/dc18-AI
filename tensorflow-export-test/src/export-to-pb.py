import os

import tensorflow as tf

modelname = os.path.join("models", "model");
meta_path = modelname + ".ckpt.meta"
output_node_names = ['outputs']
with tf.Session() as sess:
    # Restore the graph
    saver = tf.train.import_meta_graph(meta_path)
    # Load weights
    saver.restore(sess, tf.train.latest_checkpoint('models'))
    # Freeze the graph
    print(sess.graph_def)
    frozen_graph_def = tf.graph_util.convert_variables_to_constants(
        sess,
        sess.graph_def,
        output_node_names)
    print(frozen_graph_def)
    # Save the frozen graph
    with open(modelname + ".pb", 'wb') as f:
        f.write(frozen_graph_def.SerializeToString())

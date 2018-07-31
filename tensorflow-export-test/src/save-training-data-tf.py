# save-training-data-tf.py
# inspired by: https://towardsdatascience.com/deploy-tensorflow-models-9813b5a705d5
# attempted to use iris data set (downloaded using iris_data.py at
# https://github.com/tensorflow/models/blob/master/samples/core/get_started/iris_data.py)
import os

import numpy as np
import tensorflow as tf

from .iris_data import load_data

LEARNING_RATE = 0.01
SAVE_PATH = "models"
EPOCHS = 1000
# create models
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
(train_input, train_labels), (test_input, test_labels) = load_data();
tf.reset_default_graph()
# take an arbitrary number of 4x1 input matrices
x = tf.placeholder(tf.float32, shape=[None, 4], name="inputs")
# output an arbitrary number of 1x1 output predictions
y = tf.placeholder(tf.float32, shape=[None, 1], name="outputs")
train_labels = np.array(train_labels).reshape(len(train_labels), 1)
test_labels = np.array(test_labels).reshape(len(test_labels), 1)
layer1 = tf.layers.dense(x, 100, activation=tf.nn.relu)
layer2 = tf.layers.dense(layer1, 100, activation=tf.nn.relu)
pred = tf.layers.dense(layer2, 10, activation=tf.nn.sigmoid, name="prediction")
loss = tf.reduce_mean(tf.squared_difference(y, pred), name='loss')
train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss)
# this is just to ensure that retraining doesn't happen if there is a checkpoint
checkpoint = tf.train.latest_checkpoint(SAVE_PATH)
should_train = checkpoint == None
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer());
    if should_train:
        print("Training...")
        saver = tf.train.Saver();
        for epoch in range(EPOCHS):
            print("Epoch %s of %s:" % (epoch + 1, EPOCHS))
            _, curr_loss = sess.run([train_step, loss], feed_dict={x: train_input, y: train_labels})
            print("Loss this epoch is %.4f" % curr_loss)
        path = saver.save(sess, os.path.join(SAVE_PATH, "model.ckpt"))
        print("Saved at %s" % path)
    else:
        print("Restoring...")
        graph = tf.get_default_graph()
        saver = tf.train.import_meta_graph(checkpoint + '.meta')
        saver.restore(sess, checkpoint)
        loss = graph.get_tensor_by_name("loss:0")
        test_loss = sess.run(loss, feed_dict={'inputs:0': test_input, 'outputs:0': test_labels})
        print("TEST LOSS = %.4f" % test_loss)

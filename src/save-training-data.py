import tensorflow as tf
from tensorflow import keras
from tensorflow.python.saved_model import tag_constants # for saving the model

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

# NOTE: Requires IPython and Jupyter. I don't want to move off of vanilla
# Python, so I'm saving the image files instead.
# Code for saving images commented out for convenience.
#%matplotlib inline

# shorter name
fashion_mnist = keras.datasets.fashion_mnist

# get training and test images + labels
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# names of the different classes (can be indexed using the predicted class
# number found by running np.argmax over the predictions)
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#plt.figure()
#plt.imshow(train_images[0])
#plt.colorbar()
#plt.gca().grid(False)
#plt.savefig('fig1.png')

# normalize data (important to normalize both training and testing data)
train_images = train_images / 255.0
test_images = test_images / 255.0

#plt.figure(figsize=(10,10))
#for i in range(25):
#    plt.subplot(5,5,i+1)
#    plt.xticks([])
#    plt.yticks([])
#    plt.grid(False)
#    plt.imshow(train_images[i], cmap=plt.cm.binary)
#    plt.xlabel(class_names[train_labels[i]])
#plt.savefig('fig2.png')

# create a model using Keras
# https://www.tensorflow.org/guide/keras
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

# specify options for the model
model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# train the model
# this sort of training seems to be non-incremental
# in principle it should be possible to train the model incrementally, but I
# don't know how well tensorflow supports this
model.fit(train_images, train_labels, epochs=5)

# figure out how well the model did
# loss = summation of errors made
# accuracy = percentage of correctly classified images
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)

# generate predictions
predictions = model.predict(test_images)

# Plot the first 25 test images, their predicted label, and the true label
# Color correct predictions in green, incorrect predictions in red
#plt.figure(figsize=(10,10))
#for i in range(25):
#    plt.subplot(5,5,i+1)
#    plt.xticks([])
#    plt.yticks([])
#    plt.grid(False)
#    plt.imshow(test_images[i], cmap=plt.cm.binary)
#    predicted_label = np.argmax(predictions[i])
#    true_label = test_labels[i]
#    if predicted_label == true_label:
#      color = 'green'
#    else:
#      color = 'red'
#    plt.xlabel("{} ({})".format(class_names[predicted_label], 
#                                  class_names[true_label]),
#                                  color=color)
#plt.savefig('fig3.png')

# extract the first test image
img = test_images[0]
print(img.shape) # shape = number of elements in each dimension

# Not entirely sure why this is necessary, but my research indicates that it may
# be because of a certain shape format the model is expecting. However, the
# model was apparently trained on images with the same shape as the test images,
# so I have no idea, really.
# What this does, though, is add a dimension to the image, essentially
# converting the (28,28) shape to a (1,28,28) shape.
img = (np.expand_dims(img,0))
print(img.shape)

# multiple predictions on which we can call argmax
predictions = model.predict(img)
print(predictions)

# apparently the first production is the most likely one
prediction = predictions[0]

# np.argmax over the prediction results in the index of the predicted class
# this line outputs the predicted class of the test image
print(class_names[np.argmax(prediction)])

# The idea here is to try to save the training model of this network, so that it
# can be reused (in this framework or another one)
# TODO: figure out how to do this
#       - may be necessary to place the training itself within the
#         "with tf.Session()" body
#       - look into the Keras guide and figure out how the model works, see if I
#         can use it to specify this easily
#       - ideally, will be able to extract the model after use
# SOURCES:
# - https://www.tensorflow.org/guide/saved_model
# - https://stackoverflow.com/questions/33759623/tensorflow-how-to-save-restore-a-model
with tf.Graph().as_default():
    with tf.Session() as sess:
        #data_initializer = tf.placeholder(dtype=training_data.dtype,
        #                                  shape=training_data.shape)
        #label_initializer = tf.placeholder(dtype=training_labels.dtype,
        #                                   shape=training_labels.shape)
        #input_data = tf.Variable(data_initializer, trainable=False, collections=[])
        #input_labels = tf.Variable(label_initializer, trainable=False, collections=[])
        ##...
        #sess.run(input_data.initializer,
        #         feed_dict={data_initializer: training_data})
        #sess.run(input_labels.initializer,
        #         feed_dict={label_initializer: training_labels})

        # Saving
        #inputs  = { "img": img }               # TODO: fix
        #outputs = { "prediction": prediction } # TODO: fix
        #tf.saved_model.simple_save( sess, './model.ckpt', inputs, outputs)
        pass

import tensorflow as tf
from tensorflow import keras

# Helper libraries
# shorter name
fashion_mnist = keras.datasets.fashion_mnist
# we only perform training in this file
(train_images, train_labels), _ = fashion_mnist.load_data()
# names of the different classes (can be indexed using the predicted class
# number found by running np.argmax over the predictions)
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
# normalize data
train_images = train_images / 255.0
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
# NOTE: does not include optimizer because this is apparently not supported
# When loading the file, you need to recompile with a Keras optimizer
# See load-training-data.py
keras.models.save_model(model, "model.h5", overwrite=True, include_optimizer=False)
print('Model saved. Run "load-training-data.py" to test the model.')

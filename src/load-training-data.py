import tensorflow as tf
from tensorflow import keras

import numpy as np

# shorter name
fashion_mnist = keras.datasets.fashion_mnist;

# we're only testing stuff in this file
_, (test_images, test_labels) = fashion_mnist.load_data();

# names of the different classes (can be indexed using the predicted class
# number found by running np.argmax over the predictions)
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# normalize data
test_images = test_images / 255.0

# load and compile the model
model = keras.models.load_model("model.h5");

model.compile(optimizer=tf.train.AdamOptimizer(),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

# evaluate aggregate test loss/accuracy against test data
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy: %s' %(test_acc))

# find prediction for first test image
img = np.expand_dims(test_images[0], 0)   # expand dimensions bcz idk
predictions = model.predict(img)          # generate predictions for img
prediction = predictions[0]               # extract inner list from nested (singular) list
idx = np.argmax(prediction)               # find index of largest element in list

print("Actual class: %s" %(class_names[test_labels[0]])) # print the actual class of the image
print("Predicted class: %s" %(class_names[idx]))         # print the predicted class of the image

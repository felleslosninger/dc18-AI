import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn import datasets

FEATURE_SEPAL_LENGTH = 'SepalLength'
FEATURE_SEPAL_WIDTH = 'SepalWidth'
FEATURE_PETAL_LENGTH = 'PetalLength'
FEATURE_PETAL_WIDTH = 'PetalWidth'
LABEL = 'label'

# load the data set
iris = datasets.load_iris()

iris_data_w_target = [];

# add the target to the data
for i in range(len(iris.data)):
    value = np.append(iris.data[i], iris.target[i])
    iris_data_w_target.append(value)

    columns_names = [FEATURE_SEPAL_LENGTH, FEATURE_SEPAL_WIDTH, FEATURE_PETAL_LENGTH, FEATURE_PETAL_WIDTH, LABEL]

df = pd.DataFrame(data = iris_data_w_target, columns = columns_names )

# shuffle our data
df = df.sample(frac=1).reset_index(drop=True)

test_len = (len(df) * 20)//100
training_df = df[test_len:]
test_df = df[:test_len]

iris_feature_columns = [
    tf.contrib.layers.real_valued_column(FEATURE_SEPAL_LENGTH, dimension=1, dtype=tf.float32),
    tf.contrib.layers.real_valued_column(FEATURE_SEPAL_WIDTH, dimension=1, dtype=tf.float32),
    tf.contrib.layers.real_valued_column(FEATURE_PETAL_LENGTH, dimension=1, dtype=tf.float32),
    tf.contrib.layers.real_valued_column(FEATURE_PETAL_WIDTH, dimension=1, dtype=tf.float32)
]

x = {
    FEATURE_SEPAL_LENGTH : np.array(training_df[FEATURE_SEPAL_LENGTH]),
    FEATURE_SEPAL_WIDTH  : np.array(training_df[FEATURE_SEPAL_WIDTH]),
    FEATURE_PETAL_LENGTH : np.array(training_df[FEATURE_PETAL_LENGTH]),
    FEATURE_PETAL_WIDTH  : np.array(training_df[FEATURE_PETAL_WIDTH])
}

classifier = tf.estimator.DNNClassifier(
    feature_columns = iris_feature_columns,
    hidden_units = [5, 5],
    n_classes = 3)


# Define the training inputs
train_input_fn = tf.estimator.inputs.numpy_input_fn(
    x = x,
    y = np.array(training_df[LABEL]).astype(int),
    num_epochs = None,
    shuffle = True)

# Train model.
classifier.train(input_fn = train_input_fn, steps = 4000)

x = {
    FEATURE_SEPAL_LENGTH : np.array(test_df[FEATURE_SEPAL_LENGTH]),
    FEATURE_SEPAL_WIDTH  : np.array(test_df[FEATURE_SEPAL_WIDTH]),
    FEATURE_PETAL_LENGTH : np.array(test_df[FEATURE_PETAL_LENGTH]),
    FEATURE_PETAL_WIDTH  : np.array(test_df[FEATURE_PETAL_WIDTH])
}

# Define the training inputs
test_input_fn = tf.estimator.inputs.numpy_input_fn(
    x = x,
    y = np.array(test_df[LABEL]).astype(int),
    num_epochs = 1,
    shuffle = False)

# Evaluate accuracy.
accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

print("Test Accuracy: ", accuracy_score)
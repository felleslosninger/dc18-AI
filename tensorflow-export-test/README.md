# Experimental branch - save and export training data from TensorFlow to another framework

## Initializing the Docker image

On a \*nix computer (or Windows using git-bash), run the following command:

```
$ ./tensorflow.sh src
```

This kills the previous "tensorflow/tensorflow" container, if one exists, and
runs a new container. It also copies the files specified as arguments into the
container, or, if no files were specified, it copies all the files in the
current directory.

The script will output a URL with a "token" parameter. Go to that URL. You will
be brought to a Jupyter environment where the project files can be run.

## Running the project

First, ensure you have a working tensorflow/tensorflow Docker container. You 
can run `docker ps`, or just run the `./tensorflow.sh` script - it doesn't
matter if you've run it before, as the script automatically kills any
tensorflow/tensorflow containers already running.

Next, go to the URL specified at the end of the ./tensorflow.sh script.
Alternatively, you can find the URL with the required token using the
`docker logs` command, but you need to replace the docker image hash with
"localhost".

### run.ipynb

Open the file `src/run.ipynb`. Click the `Run` command in the toolbar above the
first cell to run the active cell.

## Findings

### Training, saving and loading models with TensorFlow

We've found that training a model in TensorFlow and saving the output to a H5 file
using Keras is exceedingly simple. Loading the model in another TensorFlow file
is also very simple, but it does not seem to be possible to save the compiled
optimization options along with the model. Thus, the model needs to be
recompiled upon load.

Using TensorFlow's more low-level API is also achievable, but more cumbersome.
However, this allows you more control over the model you create, which is an
advantage during the exporting step.

### Exporting pre-trained binaries to other formats

#### Conversion tools

- https://github.com/triagemd/model-converters (convert keras to tensorflow)
- https://github.com/onnx/onnx-tensorflow (convert tensorflow to onnx
  (**EXPERIMENTAL**))
- https://github.com/onnx/tensorflow-onnx (convert tensorflow to onnx
  (**EXPERIMENTAL**))

#### Limitations

The Keras to TensorFlow conversion tool (API version) requires that the second
argument is a directory name, and does not allow for specifying the name of the
saved model output file.

#### Difficulties

We found that I could not read from a saved model directly into the TensorFlow to
ONNX converter - this resulted in an `error parsing message` when calling
`graph_def.ParseFromString`. To work around this, we created a SavedModel from
the file instead, and parsed that from the string.

The next problem faced was that the tutorial for using the tf to onnx conversion
tool assumed the frozen model was created by a tool in which we explicitly
define the output; however, this is not the case when creating a saved model
using the Keras conversion tool. The tool also requires the user to specify the
name of the output node. This was found by printing the SavedModel and searching
for the string "output" - at the end of the model, the names of output and input
nodes were specified, and the name of the output node was "dense\_1/Softmax".

Following this, it was discovered that the conversion tool does not support
PlaceholderWithDefault nodes. This is apparently not a limitation within the
ONNX format (ref: https://github.com/onnx/tensorflow-onnx/pull/53/commits), but
a limitation in the conversion tool. There might be a workaround, but we
currently have no solution to this problem.

Attempting to use another TensorFlow to ONNX converter,
[tf2onnx](https://github.com/onnx/tensorflow-onnx), seems like another dead end
with this approach, as there is some other error in the saved model that it
balks at. It seems clear at this point that the added level of indirection when
using Keras is making the exporter  virtually impossible to use.

#### Working solution

**Files:**
- src/save-training-data-tf.py
- src/iris\_data.py
- src/export-to-pb.py
- src/export-to-onnx.py

We created another file which constructed its model based solely on the
TensorFlow lower level API. Saving this produced a .ckpt (chekcpoint) file,
which could be saved as a .pb (frozen graph definition) file with relative ease.
It was possible to parse the natively named .pb file (using a known output node
name) with the onnx/onnx-tensorflow conversion tool.

### Using ONNX models trained in TensorFlow with other frameworks

TODO

## TODO

- [x] Create a TensorFlow program that successfully trains a model to classify
  images
- [x] Save the model to a file
- [x] Load the model into TensorFlow (for demonstration purposes)
- [x] Convert the model to ONNX format
- [ ] Load the model in a machine learning framework supporting ONNX files

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

### Exporting pre-trained binaries to other formats

TODO: Attempt to export to ONNX format using a conversion tool
- https://github.com/triagemd/model-converters (convert keras to tensorflow)
- https://github.com/onnx/onnx-tensorflow (convert tensorflow to onnx
  (**EXPERIMENTAL**))

### Using ONNX models trained in TensorFlow with other frameworks

TODO

## TODO

- [x] Create a TensorFlow program that successfully trains a model to classify
  images
- [x] Save the model to a file
- [x] Load the model into TensorFlow (for demonstration purposes)
- [ ] Convert the model to ONNX format
- [ ] Load the model in a machine learning framework supporting ONNX files

# Experimental branch - Anaconda-based Docker machine learning environment

## Initializing the Docker image

On a \*nix computer (or Windows using git-bash), run the following command:

```
$ ./start.sh
```

This sets up a Docker image based on
[continuumio/anaconda](https://hub.docker.com/r/continuumio/anaconda/) and runs
all the required commands for this to work out of the box. See `start.sh`,
`scripts/anaconda.sh` and `scripts/docker-hash.sh` to see how the code works.

Accepts optional command line argument `--restart` which kills the previous
continuumio/anaconda image if one is running.

The script will output a URL with a "token" parameter. Go to that URL to
checkout the Jupyter notebook started by the server. From there, the project
files can be run.

## Running the project

### runAll.ipynb

This file contains six cells which demonstrates some of the approaches we have
explored in attempting to convert TensorFlow models to ONNX. The first two save
the model as a HDF5 model (Keras file format) and loads the same model to test
that it works, respectively. Previous versions of `export-to-onnx.py` attempted
to use [model\_converters](https://github.com/triagemd/model-converters) and
[onnx-tf](https://github.com/onnx/onnx-tensorflow) to convert this to ONNX, but
these efforts did not pan out.

The remaining four cells attempt to train a model using the low-level TensorFlow
API, convert this to a protobuf format, and then convert this format using
onnx-tf to ONNX format, and lastly to load the saved model into Microsoft CNTK,
which supports integrated ONNX support.

### run.ipynb and run2.ipynb

These represent old entry points to the scripts we've written.

### New notebooks

New notebooks can be created and either run existing Python code (using the
`%run ...` command) in the `src/` folder, or may contain code directly.

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
using Keras is making the exporter virtually impossible to use.

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

The problem with this approach is that currently we are unable to freeze the
graph correctly. If this error is fixed, there may be additional problems down
the line that we have not yet encountered.

### Using ONNX models trained in TensorFlow with CNTK

We attempted to use Microsoft CNTK to load the exported ONNX model. This fails
to work for two reasons:
- First, freezing the graph using `export-to-pb.py` fails; it saves an empty
  model. In theory, CNTK might be able to load that, but it turns out that
  something in the model specifies a negative dimension, which is apparently
  not supported by ONNX, which is what causes the error.
- Secondly, we tried just loading a pre-trained ONNX model found online. This
  also fails, and may be a recent issue discovered in CNTK, as documented by
  [this GitHub issue](https://github.com/Microsoft/CNTK/issues/3310) on the
  CNTK GitHub page - the error message seems to contain the same error as ours
  does.
  - Note: the model used by this file (`import-big-model-cntk.py`) is not
    included in the repo due to its size, but can be downloaded from
    [here](https://github.com/onnx/models/tree/master/bvlc_reference_caffenet).

### Using ONNX models in Caffe2

According to the [ONNX specifications](https://github.com/onnx/tutorials), Caffe2 should support exporting and importing ONNX files. We've been trying to make this work in practice, but it requires substantial configuration of an environment. We've been using various docker containers. The official Caffe2 containers are deprecated, and we could not make them work. 
We've been working from a conda container where we installed Caffe2 packages. ONNX can be installed in conda, but it needs some packages to be installed in the OS. It needs a lua package called loadcaffe which converts caffe outputs to torch-compatible files. This means that torch needs to be installed in order to use ONNX and Caffe2. 

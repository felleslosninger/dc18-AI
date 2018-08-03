# Anaconda-based Docker image for machine learning experimentation

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

The project is organized in different folders containing related source code
files and notebooks together.

### save-and-load-tensorflow-keras

This illustrates a simple example of training a model using Keras in Tensorflow,
saving the model in a HDF5 file, and reloading the saved model in a different
file to perform a prediction.

Note how the training phase can be skipped when loading the pre-trained model,
greatly shortening the execution time.


### try-export-tensorflow-to-onnx

This represents a largely unfruitful attempt at converting Tensorflow's model
format into ONNX format and loading it into a compatible framework. In part, the
lack of success sstems from difficulties with getting the other frameworks to
work properly; in part, it's due to the frameworks not playing nicely with each
other. We've found model conversion attempts cumbersome and non-robust at best,
and would advise against basing any machine learning system on the
cross-compatibility of different formats, as the support of such
cross-compatibility currently seems low.

### stillinger-nav

This represents one of two separate attempts at working with open data available
at data.norge.no, particularly data about job advertisements. The two different
notebooks contain two different approaches to training a model to categorize the
job advertisements based on labeled training data: one uses Sklearn, while the
other uses FastText.

The model works by leveraging the tendency of different kinds of documents to
use specific language. Words which are common in one category but not in the
others are characteristic for documents in that category, and documents
containing those wordsare lmore likely to be predicted to belong to sai
category. Over time, with lots of data samples, the model learns what sorts of
words belong to which category.

We experienced a fair degree of success with  this algorithm. Furthermore, it's
a simple but broadly applicable learning model which would be able to work on
many different datasets in order to group them into different categories.

### job-ads-unlabeled-topic-modeling

This notebook contains the other attempt at working with the job ad data from
data.norge.no. In particular, it treats the job description text as unlabeled
data and attempts to extract topics from the model.

The algorithm uses a form of topic modeling with
[latent Dirichlet allocation (LDA)](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)
in order to construct a predictive model, again leveraging the fact that
different topics tend to use different words to describe their content. We
constructed two different models: one based on just a regular bag of words
across all documents, and one based on TF-IDF over that bag of words. The
algorithm was told to generate 10 topics - this number was an arbitrary decision
by the programmer.

We received some interesting results. Among the topics determined by the
algorithm, some could easily be classified as belonging to a specific job
category, and three team members independently assigned them the same labels.
This included jobs related to children, jobs related to health, customer service
jobs, leadership positions and educational jobs. Some other categories seemed to
be about information provided or sought in the ad itself - such as contact
information, information about who provided the ad, as well as information
sought about potential applicants. Interestingly, the models also determined
that English and, in the case of the bag of words model, nynorsk, were topics in
their own right.

There are some obvious limitations to this algorithm. For one, it's not able to
automatically label the topic, and it's not alway  obvious what a topic
concerns at a glance. Second, the fact that the number of topics to search for
is determined by the programmer means that in order to have a meaningful set of
topics, a good guess for the number of topics in the documents is required. It
could be interesting to try and connect this model to a topic map - for instance
[Los](https://www.difi.no/fagomrader-og-tjenester/digitalisering-og-samordning/nasjonal-arkitektur/los),
in order to see if we could automatically label the topics based on which words
are important.

### New notebooks

New notebooks can be created and either run existing Python code (using the
`%run ...` command) in the `src/` folder, or may contain code directly.

## Findings

**NOTE:** This section is largely focused on the interoperability of the
different deep learning frameworks and models. Our results within text document
classification are better described elsewhere - see comments in the notebooks
and descriptions in the report on this project.

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

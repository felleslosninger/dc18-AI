#!/bin/bash

FIND_RUNNING="$(find . | grep docker-hash) continuumio/anaconda"

IMGHASH="$(eval $FIND_RUNNING)"
if [ ! "$IMGHASH" ]; then
    echo "Starting anaconda docker container"
    docker run -p 8888:8888 -it -d continuumio/anaconda /bin/bash > /dev/null
    IMGHASH="$(eval $FIND_RUNNING)"
    echo "Docker container with hash $IMGHASH started"
    echo "" # newline
fi

echo -n "Installing system packages... "
docker exec -ti "$IMGHASH" /bin/bash -c "apt-get update > /dev/null && apt-get install -y \
    libopencv-dev python-opencv openmpi-bin libopenmpi-dev > /dev/null"
echo "done"

echo -n "Upgrading pip... "
docker exec -ti "$IMGHASH" /bin/bash -c "pip install -U pip > /dev/null"
echo "done"
echo "Installing additional modules:"
for module in "onnx" "tensorflow" "model_converters" "onnx-tf" "cntk" "html" "wget" "gensim" "nltk"
do
    echo -n "$module... "
    docker exec -ti "$IMGHASH" /bin/bash -c "pip install -U $module > /dev/null"
    echo "done"
done
echo "" # newline

# ensure that the /opt/notebooks folder exists and is empty
docker exec -it "$IMGHASH" /bin/bash -c "mkdir -p /opt/notebooks/ && rm -rf /opt/notebooks/*"

if [[ $# < 1 ]]; then
    # default: copy all files in the folder
    echo "Copying all files to anaconda directory..."
    tar -cv * | docker exec -i "$IMGHASH" tar x -C /opt/notebooks
else
    # if arguments present: try to copy each file given as an argument
    echo "Copying specified files to anaconda directory..."
    for arg in "$@"
    do
        if [ -f "$arg" ] || [ -d "$arg" ]; then
            # file exists
            tar -cv "$arg" | docker exec -i "$IMGHASH" tar x -C /opt/notebooks
            # SOURCE: https://stackoverflow.com/a/28123384
        else
            # file doesn't exist
            echo "File $arg does not exist; skipping"
        fi
    done
fi
echo "" # newline

# create a couple of symlinks so that the system doesn't complain
for f in "libmpi.so.12" "libmpi_cxx.so.1"
do
    docker exec -it "$IMGHASH" /bin/bash -c \
        "ln -s /usr/lib/x86_64-linux-gnu/openmpi/lib/${f%.*} /usr/lib/$f" > /dev/null 2>&1
done

# load the start-jupyter.sh script which runs the Jupyter notebook and displays
# the correct url to navigate to
tar -cv scripts/start-jupyter.sh 2>/dev/null | docker exec -i "$IMGHASH" tar x -C .

docker exec -it "$IMGHASH" /bin/bash -c "./scripts/start-jupyter.sh"

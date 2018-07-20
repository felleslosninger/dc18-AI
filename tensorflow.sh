#!/bin/bash

# NOTE: This creates a tensorflow docker image and copies files into the image's
# directory. This allows the user to create and initialize a docker image
# automatically

if [ -f kill-tensorflow.sh ]; then
    echo "Running kill script to kill old tensorflow container"
    ./kill-tensorflow.sh
    echo "" # newline
fi

# create a docker image of tensorflow
echo "Starting docker container of tensorflow"
# NOTE: Sleeping for 0.2 seconds to give docker time to properly kill the server
# If I don't, I tend to get an error claiming the port is already in use
docker run -p 8888:8888 -d tensorflow/tensorflow > /dev/null

# find the hash of the image for future docker commands
IMGHASH="$(docker ps | grep tensorflow/tensorflow | sed -n 's/\(............\).*/\1/p')"
echo "Docker container with hash $IMGHASH started"
echo "" # newline

if [[ $# < 1 ]]; then
    # default: copy all files in the folder
    echo "Copying all files to tensorflow directory..."
    tar -cv * | docker exec -i "$IMGHASH" tar x -C .
else
    # if arguments present: try to copy each file given as an argument
    echo "Copying specified files to tensorflow directory..."
    for arg in "$@"
    do
        if [ -f "$arg" ] || [ -d "$arg" ]; then
            # file exists
            tar -cv "$arg" | docker exec -i "$IMGHASH" tar x -C .
            # SOURCE: https://stackoverflow.com/a/28123384
        else
            # file doesn't exist
            echo "File $arg does not exist; skipping"
        fi
    done
fi
echo "" # newline

# Sleep for one second so the container will have time to start, then output the
# URL the user has to go to in order to run the files
# This is necessary because Jupyter requires the user to go to a specific URL
# using a random token for security purposes (or else, enable a password, but
# this seems easier).

# NOTE: The time required to sleep is no more than 1 second on my computer, but
# this might need to be changed on a different computer, or might be different
# the first time the program runs.
sleep 1 && echo -n "URL: " && docker logs "$IMGHASH" 2>&1 | grep "http://$IMGHASH" | \
    sed -n '1 s/.*\(http:\/\/'"$IMGHASH"'.*\)/\1/p' | sed -n 's/'"$IMGHASH"'/localhost/p' &

# Create a "kill" script for easily killing the container
echo "docker kill $IMGHASH && rm \$0" > kill-tensorflow.sh && chmod +x kill-tensorflow.sh
echo "Run ./kill-tensorflow.sh to kill the docker container"

wait # wait for background process (printing URL with token) to finish

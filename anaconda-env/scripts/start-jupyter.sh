#!/bin/bash

# NOTE: This file exists in order to have more control over the Jupyter starting
# process; specifically, we want it to run in the background but still display
# parts of its output (but replacing the container's hash with "localhost")

if [ ! -f "/opt/conda/bin/jupyter" ]; then
    echo "Installing Jupyter..."
    /opt/conda/bin/conda install jupyter -y --quiet > /dev/null
    echo "" # newline
fi

echo "Starting Jupyter notebook..."
/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks \
    --ip='*' --port=8888 --no-browser --allow-root > jupyter.log 2>&1 &

echo "Waiting for URL..."
while ! (cat jupyter.log | grep http > /dev/null)
do
    sleep 1
done
echo -n "URL: "
echo "$(cat jupyter.log | grep http | sed -n '1 s/.*\(http:\/\/\)[a-f0-9]*\(:8888.*\)/\1localhost\2/p')"
wait

#!/bin/bash
if [ $(echo "$@" | grep -e "--restart") ]; then
    DOCKER_IMG=$(scripts/docker-hash.sh continuumio/anaconda)
    if [ "$DOCKER_IMG" ]; then
        echo "Killing existing docker image ($DOCKER_IMG)"
        docker kill "$DOCKER_IMG" > /dev/null
        echo "" # newline
    fi
fi
scripts/anaconda.sh src models

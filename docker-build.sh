#!/usr/bin/env bash

# This script build a local docker for tests

local_docker="black-widow:local"

# Remove current docker image
docker rmi "${local_docker}"
# Build new docker image
docker build -t "${local_docker}" .
# Run new docker image and than, remove it
echo
echo
echo "Done!"
echo
echo "To run the new docker image, launch:"
echo
echo "    docker run --rm ${local_docker}"
echo

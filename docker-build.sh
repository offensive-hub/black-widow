#!/usr/bin/env bash

# This script build a local docker for tests

find . -name *.pyc -exec rm -rf {} \; 2> /dev/null
find . -name __pycache__ -exec rm -rf {} \; 2> /dev/null

local_docker="black-widow:local" 2> /dev/null

# Remove current docker image
docker rmi "${local_docker}"
# Build new docker image
docker build -t "${local_docker}" --network=host .
# Run new docker image and than, remove it
echo
echo
echo "Done!"
echo
echo "To run the new docker image, launch:"
echo
echo "    [GUI]: ./docker-gui.sh"
echo "    [CMD]: ./docker-cmd.sh"
echo

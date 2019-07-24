#!/usr/bin/env bash

# This script build a local docker for tests

# Remove current docker image
docker rmi black-widow:local
# Build new docker image
docker build -t black-widow:local .
# Run new docker image and than, remove it
docker run --rm black-widow:local

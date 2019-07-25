#!/usr/bin/env bash

# This script start a local docker for tests

local_docker="black-widow:local"

docker run --rm "${local_docker}" "$@"

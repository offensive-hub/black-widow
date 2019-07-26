#!/usr/bin/env bash

# This script start a local docker for tests

local_docker="black-widow:local"

docker run -d -p 8000:80 --rm "${local_docker}" -g

#!/usr/bin/env bash

# This script start a local docker for tests

local_docker="black-widow:local"

# -d
docker run -p 8095:8095 --rm "${local_docker}" -g
#!/usr/bin/env bash

# This script start a local docker for tests

local_docker="black-widow:local"
port='8095'

docker run -d -it -p "${port}:80" --rm "${local_docker}" "$@"

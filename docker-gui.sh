#!/usr/bin/env bash

# This script start a local docker for tests

local_docker="black-widow:local"
host='127.0.0.1'
port='8095'

# Usage "-p": <port_localhost>:<port_docker>
docker run -d -p "${host}:${port}" --rm "${local_docker}" -g
echo "Listening on http://${host}:${port}"

#!/usr/bin/env bash

# This script start a local docker for tests

main() {
    local local_docker="black-widow:local"
    local host='127.0.0.1'
    local port='8095'

    # Usage "-p": <port_localhost>:<port_docker>
    docker run -d -it -p "${port}:80" --rm "${local_docker}" -g
    echo "Listening on http://${host}:${port}"

    local container=`docker ps | grep "${local_docker}" | awk '{print $1;}'`
    echo "To enter in docker:"
    echo "docker exec -it ${container} sh"
    echo ""
}

main

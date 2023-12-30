#!/bin/bash

set -e

DEFAULT_DEBIAN_NAME="bullseye"
DEFAULT_PYTHON_VERSION="3.9"
DEFAULT_PYTHON_DISTROLESS_IMAGE="al3xos/python-distroless:3.9-debian11"

print_usage() {
    echo "Usage: $(basename "$0") <build|local|env>"
    exit 1
}

build() {
    local debian_name="${DEBIAN_NAME:-$DEFAULT_DEBIAN_NAME}"
    local python_version="${PYTHON_VERSION:-$DEFAULT_PYTHON_VERSION}"
    local distroless_image="${PYTHON_DISTROLESS_IMAGE:-$DEFAULT_PYTHON_DISTROLESS_IMAGE}"

    docker build \
        --build-arg=DEBIAN_NAME="$debian_name" \
        --build-arg=PYTHON_VERSION="$python_version" \
        --build-arg=PYTHON_DISTROLESS_IMAGE="$distroless_image" \
        -t phrasee-app .
}

run() {
    build
    # Stop the container if it is running
    docker ps -q --filter "ancestor=phrasee-app" | xargs -r docker stop
    # Run the container
    docker run --rm -p 5000:5000 phrasee-app
}


# Main script logic
case "$1" in
"build")
    build
    ;;
"local")
    run
    ;;
*)
    print_usage
    ;;
esac

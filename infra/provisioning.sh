#!/bin/bash
 
set -e

print_usage() {
    echo "Usage: $(basename $0) <synth|deploy|destroy|env>"
    exit 1
}

get_public_ip() {
    local ip=$(curl -s ifconfig.me)

    if [[ -z "$ip" ]]; then
        echo "$(basename $0) - get_public_ip - could not retrieve public IP address" >&2
        exit 1
    fi

    echo "$ip"
}

to_cidr() {
    echo "$1/32"
}

prepare_cdktf_environment() {
    export MY_IP_ADDRESS=$(to_cidr $(get_public_ip))
    export AWS_PROFILE="aqoon" # CHANGE
    export S3_BUCKET_NAME="phrasee-cdktf" # CHANGE
}

synth() {
    prepare_cdktf_environment
    echo "Synthesising with MY_IP_ADDRESS=$MY_IP_ADDRESS"
    npx cdktf synth NetworkingStack EcsStack
}

deploy() {
    prepare_cdktf_environment
    echo "Deploying with MY_IP_ADDRESS=$MY_IP_ADDRESS"
    npx cdktf deploy NetworkingStack EcsStack
}

destroy() {
    prepare_cdktf_environment
    npx cdktf destroy NetworkingStack EcsStack
}

if [ -z "$1" ]; then
    print_usage
fi

case "$1" in
    synth)
        synth
        ;;
    deploy)
        deploy
        ;;
    destroy)
        destroy
        ;;
    env)
        prepare_cdktf_environment
        ;;
    *)
        echo "$(basename $0) - invalid option: $1" >&2
        print_usage
        ;;
esac
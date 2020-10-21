#!/bin/sh

DATE="$(date "+%Y%m%d%H%M")"
SERVICE_NAME="latonaio/stream-usb-thermo-by-grpc-client"
DOCKER_BUILDKIT=1 docker build -f Dockerfile-client -t ${SERVICE_NAME}:${DATE} .
docker tag ${SERVICE_NAME}:${DATE} ${SERVICE_NAME}:latest

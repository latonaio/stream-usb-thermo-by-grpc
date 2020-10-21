#!/bin/bash

IMAGE_NAME="latonaio/stream-usb-thermo-by-grpc-base"

docker build -f Dockerfile-base -t ${IMAGE_NAME}:latest .

#!/bin/bash

set -e

IMAGE_NAME="enao-genre-scraper"
DOCKER_HUB_USER="wildanazz"
DOCKER_TAG="latest"
FULL_IMAGE_NAME="$DOCKER_HUB_USER/$IMAGE_NAME:$DOCKER_TAG"

echo "Building the Docker image..."
docker build -t "$IMAGE_NAME" .

echo "Tagging the Docker image as $FULL_IMAGE_NAME..."
docker tag "$IMAGE_NAME" "$FULL_IMAGE_NAME"

echo "Pushing the Docker image to Docker Hub..."
docker push "$FULL_IMAGE_NAME"

echo "Docker image has been built, tagged, and pushed successfully."
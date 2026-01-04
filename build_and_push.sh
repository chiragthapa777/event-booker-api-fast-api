#!/bin/bash
set -e

# ---- CONFIGURATION ----
IMAGE_NAME="chiragthapa777/event-booker"
TAG="v1.0.0"  # You can also use: TAG=$(git rev-parse --short HEAD)
DOCKERFILE="Dockerfile"

# ---- CHECK FOR BUILDX ----
if ! docker buildx version &> /dev/null; then
  echo "❌ Docker Buildx is not available. Please enable experimental features in Docker."
  exit 1
fi

# ---- LOGIN (if not logged in) ----
if ! docker info | grep -q "Username:"; then
  echo "🔑 Logging into Docker Hub..."
  docker login || { echo "❌ Login failed"; exit 1; }
else
  echo "✅ Already logged into Docker Hub"
fi

# ---- CREATE BUILDX BUILDER (if missing) ----
if ! docker buildx inspect multiarch-builder &>/dev/null; then
  echo "🧱 Creating a new multi-architecture builder..."
  docker buildx create --name multiarch-builder --use
else
  docker buildx use multiarch-builder
fi

# ---- BUILD & PUSH ----
echo "🏗️  Building and pushing multi-architecture image..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ${IMAGE_NAME}:${TAG} \
  -t ${IMAGE_NAME}:latest \
  -f ${DOCKERFILE} \
  --push .

# ---- DONE ----
echo "✅ Successfully built and pushed:"
echo "   - ${IMAGE_NAME}:${TAG}"
echo "   - ${IMAGE_NAME}:latest"

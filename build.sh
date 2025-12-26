#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAG="${1:-local/remote-project-manager}"
RPM_VERSION="${RPM_VERSION:-v0.1.0}"

cd "$ROOT_DIR"

echo "Building add-on image: $TAG (RPM_VERSION=$RPM_VERSION)"

docker build \
  --build-arg RPM_VERSION="$RPM_VERSION" \
  -t "$TAG" \
  .

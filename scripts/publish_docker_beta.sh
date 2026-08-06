#!/usr/bin/env bash
# Builds the Mosfet Docker image and pushes it to Docker Hub as the beta tag.

# exit on error, error on unset vars, fail pipelines on first error
set -euo pipefail

# =============================================================================
# Phase 0: Configuration
# =============================================================================

IMAGE="busycaesar/mosfet:beta"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# =============================================================================
# Phase 1: Helper functions
# =============================================================================

err() {
    echo "Error: $1" >&2  # print message to stderr
    exit 1                # abort the script with a non-zero status
}

# =============================================================================
# Phase 2: Prerequisite checks
# =============================================================================

command -v docker >/dev/null 2>&1 || err "docker is required but not installed."

# =============================================================================
# Phase 3: Build
# =============================================================================

echo "Building $IMAGE..."
docker build -t "$IMAGE" "$REPO_DIR"

# =============================================================================
# Phase 4: Push
# =============================================================================

echo "Pushing $IMAGE..."
docker push "$IMAGE"

# =============================================================================
# Phase 5: Done
# =============================================================================

echo
echo "Published $IMAGE."

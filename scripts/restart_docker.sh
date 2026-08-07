#!/usr/bin/env bash
# Takes down any running Mosfet containers, then starts a fresh one in the background.

# exit on error, error on unset vars, fail pipelines on first error
set -euo pipefail

# =============================================================================
# Phase 0: Configuration
# =============================================================================

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
# Phase 3: Down
# =============================================================================

echo "Stopping any running Mosfet containers..."
docker compose -f "$REPO_DIR/docker-compose.yml" down --remove-orphans

# =============================================================================
# Phase 4: Up
# =============================================================================

echo "Starting Mosfet..."
docker compose -f "$REPO_DIR/docker-compose.yml" up -d

# =============================================================================
# Phase 5: Done
# =============================================================================

echo
echo "Mosfet is running."

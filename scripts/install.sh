#!/usr/bin/env bash
# Installs Mosfet into ~/.mosfet and puts a `mosfet` launcher on PATH.

# exit on error, error on unset vars, fail pipelines on first error
set -euo pipefail

# =============================================================================
# Phase 0: Configuration
# =============================================================================

REPO_URL="https://github.com/busycaesar/Mosfet.git"
INSTALL_DIR="$HOME/.mosfet"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/mosfet"

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

command -v git >/dev/null 2>&1 || err "git is required but not installed."
command -v python3 >/dev/null 2>&1 || err "python3 is required but not installed."

# =============================================================================
# Phase 3: Clone or update the repository (always the latest release tag)
# =============================================================================

# Latest release = highest vX.Y.Z git tag, not whatever HEAD of a branch
# happens to be — keeps installs pinned to tagged releases only.
LATEST_TAG="$(git ls-remote --tags --refs "$REPO_URL" | awk '{print $2}' | sed 's#refs/tags/##' | sort -V | tail -n1)"
[ -n "$LATEST_TAG" ] || err "No release tags found in $REPO_URL."

if [ -d "$INSTALL_DIR/.git" ]; then
    # Already a git repo: make sure it's actually our repo, then update it.
    origin_url="$(git -C "$INSTALL_DIR" remote get-url origin)"
    [ "$origin_url" = "$REPO_URL" ] || err "$INSTALL_DIR exists and is not a Mosfet clone (origin: $origin_url)."

    current_tag="$(git -C "$INSTALL_DIR" describe --tags --exact-match 2>/dev/null || true)"
    if [ "$current_tag" = "$LATEST_TAG" ]; then
        echo "Already on latest release ($LATEST_TAG)."
    else
        echo "Updating to $LATEST_TAG..."

        git -C "$INSTALL_DIR" fetch --tags origin
        git -C "$INSTALL_DIR" checkout "$LATEST_TAG"
    fi
elif [ -e "$INSTALL_DIR" ]; then
    # Path exists but isn't a git repo: refuse to touch it.
    err "$INSTALL_DIR already exists and is not a git repository. Remove it and re-run this script."
else
    # Fresh install: clone the latest release tag.
    echo "Cloning Mosfet $LATEST_TAG into $INSTALL_DIR..."

    git clone --branch "$LATEST_TAG" "$REPO_URL" "$INSTALL_DIR"
fi

# =============================================================================
# Phase 4: Python virtual environment setup
# =============================================================================

echo "Setting up Python virtual environment..."

# create the venv only if it doesn't already exist
[ -d "$VENV_DIR" ] || python3 -m venv "$VENV_DIR"

"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/req.txt" -q

# =============================================================================
# Phase 5: Provider and credentials setup (mosfet.config.json + .env)
# =============================================================================

# Interactive arrow-key selection (same pattern as Claude Code's own setup
# prompts) — handled by a Python helper since it's far more robust than
# hand-rolling terminal escape-sequence handling in bash, and python3 is
# already a hard prerequisite of this script.
#
# Piping this script via `curl | bash` consumes stdin to read the script
# itself, so the prompts must read from the controlling terminal directly
# instead of inherited stdin.
if [ -r /dev/tty ]; then
    "$VENV_DIR/bin/python3" "$INSTALL_DIR/scripts/setup_provider.py" < /dev/tty
else
    echo "No interactive terminal detected — skipping provider setup."
    echo "Run 'python3 $INSTALL_DIR/scripts/setup_provider.py' later to configure Mosfet."
fi

# =============================================================================
# Phase 6: Launcher installation
# =============================================================================

echo "Installing launcher to $LAUNCHER..."
mkdir -p "$BIN_DIR"  # ensure the target bin directory exists
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python" "$INSTALL_DIR/src/main.py" "\$@"
EOF
chmod +x "$LAUNCHER"  # make the launcher executable

echo
echo "Mosfet installed successfully."

# =============================================================================
# Phase 7: PATH check
# =============================================================================

case ":$PATH:" in
    *":$BIN_DIR:"*) ;;  # BIN_DIR is already on PATH: nothing to do
    *)
        # BIN_DIR is missing from PATH: tell the user how to add it.
        echo
        echo "Warning: $BIN_DIR is not on your PATH."
        echo "Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
        echo "    export PATH=\"$BIN_DIR:\$PATH\""
        ;;
esac

# =============================================================================
# Phase 8: Done
# =============================================================================

echo
echo "Run 'mosfet' from anywhere to start chatting."
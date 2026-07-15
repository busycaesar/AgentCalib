#!/usr/bin/env bash
# Installs Mosfet into ~/.mosfet and puts a `mosfet` launcher on PATH.

# exit on error, error on unset vars, fail pipelines on first error
set -euo pipefail

# =============================================================================
# Phase 0: Configuration
# =============================================================================

REPO_URL="https://github.com/busycaesar/Mosfet.git"
BRANCH="Master"
INSTALL_DIR="$HOME/.mosfet"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/mosfet"
ENV_FILE="$INSTALL_DIR/.env"

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
# Phase 3: Clone or update the repository
# =============================================================================

if [ -d "$INSTALL_DIR/.git" ]; then
    # Already a git repo: make sure it's actually our repo, then update it.
    origin_url="$(git -C "$INSTALL_DIR" remote get-url origin)"
    [ "$origin_url" = "$REPO_URL" ] || err "$INSTALL_DIR exists and is not a Mosfet clone (origin: $origin_url)."

    echo "Updating existing installation..."

    git -C "$INSTALL_DIR" pull --ff-only origin "$BRANCH"
elif [ -e "$INSTALL_DIR" ]; then
    # Path exists but isn't a git repo: refuse to touch it.
    err "$INSTALL_DIR already exists and is not a git repository. Remove it and re-run this script."
else
    # Fresh install: clone the repo for the first time.
    echo "Cloning Mosfet into $INSTALL_DIR..."

    git clone --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
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
# Phase 5: Credentials setup (.env)
# =============================================================================

# No .env yet: prompt the user for their OpenAI credentials.
if [ ! -f "$ENV_FILE" ]; then
    echo
    echo "Enter your OpenAI credentials"
    # -s hides input (secret), -r avoids backslash escaping
    read -r -s -p "OPENAI_API_KEY: " openai_api_key
    echo
    read -r -s -p "OPENAI_ORG_ID: " openai_org_id
    read -r -s -p "OPENAI_PROJECT: " openai_project

    # warn but don't fail the install
    [ -n "$openai_api_key" ] || echo "Warning: no API key entered. Edit $ENV_FILE before running mosfet."

    # store the secrects in .env file.
    cat > "$ENV_FILE" <<EOF
OPENAI_API_KEY="$openai_api_key"
OPENAI_ORG_ID="$openai_org_id"
OPENAI_PROJECT="$openai_project"
EOF

    # restrict permissions since the file holds secrets
    chmod 600 "$ENV_FILE"
else
    # .env already present: don't overwrite existing credentials.
    echo ".env already exists, skipping credential prompt."

    # warn if the existing .env is missing the required API key
    grep -qE '^OPENAI_API_KEY="[^"]+"' "$ENV_FILE" || echo "Warning: OPENAI_API_KEY is missing or empty in $ENV_FILE. Edit it before running mosfet."
fi

# =============================================================================
# Phase 6: Launcher installation
# =============================================================================

echo "Installing launcher to $LAUNCHER..."
mkdir -p "$BIN_DIR"  # ensure the target bin directory exists
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python" "$INSTALL_DIR/src/main.py"
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
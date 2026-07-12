#!/usr/bin/env bash
# Installs Mosfet into ~/.mosfet and puts a `mosfet` launcher on PATH.
set -euo pipefail

REPO_URL="https://github.com/busycaesar/Mosfet.git"
BRANCH="Master"
INSTALL_DIR="$HOME/.mosfet"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/mosfet"
ENV_FILE="$INSTALL_DIR/.env"

err() {
    echo "Error: $1" >&2
    exit 1
}

command -v git >/dev/null 2>&1 || err "git is required but not installed."
command -v python3 >/dev/null 2>&1 || err "python3 is required but not installed."

if [ -d "$INSTALL_DIR/.git" ]; then
    origin_url="$(git -C "$INSTALL_DIR" remote get-url origin)"
    [ "$origin_url" = "$REPO_URL" ] || err "$INSTALL_DIR exists and is not a Mosfet clone (origin: $origin_url)."

    echo "Updating existing installation..."
    git -C "$INSTALL_DIR" pull --ff-only origin "$BRANCH"
elif [ -e "$INSTALL_DIR" ]; then
    err "$INSTALL_DIR already exists and is not a git repository. Remove it and re-run this script."
else
    echo "Cloning Mosfet into $INSTALL_DIR..."
    git clone --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
fi

echo "Setting up Python virtual environment..."
[ -d "$VENV_DIR" ] || python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/req.txt" -q

if [ ! -f "$ENV_FILE" ]; then
    echo
    echo "Enter your OpenAI credentials (leave org/project blank to skip):"
    read -r -s -p "OPENAI_API_KEY: " openai_api_key
    echo
    read -r -s -p "OPENAI_ORG_ID: " openai_org_id
    read -r -s -p "OPENAI_PROJECT: " openai_project

    [ -n "$openai_api_key" ] || echo "Warning: no API key entered. Edit $ENV_FILE before running mosfet."

    cat > "$ENV_FILE" <<EOF
OPENAI_API_KEY="$openai_api_key"
OPENAI_ORG_ID="$openai_org_id"
OPENAI_PROJECT="$openai_project"
EOF
    chmod 600 "$ENV_FILE"
else
    echo ".env already exists, skipping credential prompt."
fi

echo "Installing launcher to $LAUNCHER..."
mkdir -p "$BIN_DIR"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python" "$INSTALL_DIR/src/main.py"
EOF
chmod +x "$LAUNCHER"

echo
echo "Mosfet installed successfully."

case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *)
        echo
        echo "Warning: $BIN_DIR is not on your PATH."
        echo "Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
        echo "    export PATH=\"$BIN_DIR:\$PATH\""
        ;;
esac

echo
echo "Run 'mosfet' from anywhere to start chatting."

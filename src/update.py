import os
import subprocess
import sys
from config import ROOT_PATH

def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT_PATH), *args], capture_output=True, text=True)

def run_update():
    if os.path.exists("/.dockerenv"):
        print("Mosfet is running in Docker. To update, run this on the host instead:")
        print("  docker compose pull && docker compose up -d")
        return

    if not (ROOT_PATH / ".git").is_dir():
        print(f"Can't update: {ROOT_PATH} isn't a git checkout of Mosfet.")
        sys.exit(1)

    status = _git("status", "--porcelain")

    if status.stdout.strip():
        print(f"{ROOT_PATH} has local changes. Commit or discard them before updating.")
        sys.exit(1)

    # install.sh already knows how to fetch/compare/checkout/reinstall deps for an existing install. Reuse it instead of a second implementation, pinned to this install's own directory via MOSFET_INSTALL_DIR.
    install_script = ROOT_PATH / "scripts" / "install.sh"

    env = {**os.environ, "MOSFET_INSTALL_DIR": str(ROOT_PATH)}
    result = subprocess.run(["bash", str(install_script)], env=env)

    if result.returncode != 0:
        sys.exit(result.returncode)
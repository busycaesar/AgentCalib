import argparse
from ui import run_cli_chat, run_discord_chat

UI = "CLI" # CLI, Web, Discord

def parse_args():
    parser = argparse.ArgumentParser(description="Run Mosfet with the given interface.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--cli", action="store_const", dest="ui", const="CLI")
    group.add_argument("--discord", action="store_const", dest="ui", const="Discord")
    parser.set_defaults(ui=UI)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.ui == "CLI":
        run_cli_chat()
    elif args.ui == "Discord":
        run_discord_chat()
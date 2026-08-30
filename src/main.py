import argparse
from config_setup import run_config
from ui import add_communications_arguments, run_communications
from update import run_update

def parse_args():
    parser = argparse.ArgumentParser(description="Run Mosfet with the given interface.")
    subparsers = parser.add_subparsers(dest="command")

    # Config
    subparsers.add_parser("config", help="Create or update mosfet.config.json and .env")

    # Update
    subparsers.add_parser("update", help="Update Mosfet to the latest release.")

    # DEFAULT
    add_communications_arguments(subparsers)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.command == "config":
        run_config()
    elif args.command == "update":
        run_update()
    else:
        run_communications(args)

import sys

from config.paths import CONFIG_PATH

UI = "CLI" # CLI, Web, Discord

def add_communications_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--cli", action="store_const", dest="ui", const="CLI")
    group.add_argument("--discord", action="store_const", dest="ui", const="Discord")
    parser.set_defaults(ui=UI)

def run_communications(args):
    if not CONFIG_PATH.is_file():
        print("No config found. Run 'mosfet config' to set up Mosfet.")
        sys.exit(1)

    from ui import run_cli_chat, run_discord_chat

    if args.ui == "CLI":
        run_cli_chat()
    elif args.ui == "Discord":
        run_discord_chat()
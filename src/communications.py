from config_setup import check_config
from ui import run_cli_chat, run_discord

def add_communications_arguments(subparsers):
    # Discord
    discord_parser = subparsers.add_parser("discord", help="Chat via Discord.")
    discord_parser.add_argument("--foreground", "-f", action="store_true", help="Run Discord attached to this terminal instead of in the background.")
    discord_parser.add_argument("--stop", action="store_true", help="Stop a background Discord bot.")

def run_communications(args):
    check_config()

    if args.command == "discord":
        run_discord(foreground=args.foreground, stop=args.stop)
    else:
        run_cli_chat()
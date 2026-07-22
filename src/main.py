from ui import run_cli_chat, run_discord_chat

UI = "Discord" # CLI, Web, Discord

if __name__ == "__main__":
    if UI == "CLI":
        run_cli_chat()
    elif UI == "Discord":
        run_discord_chat()
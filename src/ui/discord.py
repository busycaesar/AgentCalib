import os
import sys
import signal
import subprocess
import discord
from core import parse_user_input, messages
from config import DISCORD_BOT_TOKEN, DISCORD_MESSAGE_LIMIT, RUNTIME_PATH, DISCORD_LOG_PATH, DISCORD_PID_PATH

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def send_long_message(channel, text):
    """
    Discord throws error for messages beyond 2000 characters.
    Hence breaking the long messages beyond 2000 characters into multiple messages.
    """
    for i in range(0, len(text), DISCORD_MESSAGE_LIMIT):
        await channel.send(text[i:i + DISCORD_MESSAGE_LIMIT])

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

@client.event
async def on_message(message):
    # Ensure that it does not reply to itself.
    if message.author == client.user:
        return

    # Ensure only direct messages are allowed.
    if not isinstance(message.channel, discord.DMChannel):
        return

    async with message.channel.typing():
        try:
            response = parse_user_input(messages, message.content)
        except Exception as error:
            await message.channel.send(f"Error: {error}. Please try again.")
            return

    await send_long_message(message.channel, response)

def run_discord(foreground=False, stop=False):
    if stop:
        stop_discord_in_background()
    elif foreground:
        run_discord_chat()
    else:
        run_discord_in_background()

def run_discord_chat():
    if not DISCORD_BOT_TOKEN:
        raise RuntimeError("DISCORD_BOT_TOKEN is not set. Add it to your .env file before running Mosfet.")

    client.run(DISCORD_BOT_TOKEN)

def run_discord_in_background():
    if DISCORD_PID_PATH.is_file():
        pid = int(DISCORD_PID_PATH.read_text())

        if _is_running(pid):
            print(f"Discord bot is already running in background (PID {pid}).")
            return

    RUNTIME_PATH.mkdir(parents=True, exist_ok=True)

    with open(DISCORD_LOG_PATH, "a") as log_file:
        process = subprocess.Popen(
            [sys.executable, sys.argv[0], "discord", "--foreground"],
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )

    DISCORD_PID_PATH.write_text(str(process.pid))

    print(f"Discord bot started in background (PID {process.pid}). Logs: {DISCORD_LOG_PATH}")

def stop_discord_in_background():
    if not DISCORD_PID_PATH.is_file() or not _is_running(int(DISCORD_PID_PATH.read_text())):
        print("No background Discord bot is running.")
        return

    pid = int(DISCORD_PID_PATH.read_text())
    os.kill(pid, signal.SIGTERM)
    DISCORD_PID_PATH.unlink(missing_ok=True)

    print(f"Stopped Discord bot (PID {pid}).")

def _is_running(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
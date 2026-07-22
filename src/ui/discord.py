import os
import discord
from dotenv import load_dotenv
from core import parse_user_input, messages
from config import GOODBYE_MESSAGE

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_ALLOWED_USER_ID = os.getenv("DISCORD_ALLOWED_USER_ID")

DISCORD_MESSAGE_LIMIT = 2000

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def send_long_message(channel, text):
    for i in range(0, len(text), DISCORD_MESSAGE_LIMIT):
        await channel.send(text[i:i + DISCORD_MESSAGE_LIMIT])

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    if str(message.author.id) != DISCORD_ALLOWED_USER_ID:
        return

    if message.content.strip().lower() in ("exit", "quit"):
        await message.channel.send(GOODBYE_MESSAGE)
        await client.close()
        return

    async with message.channel.typing():
        try:
            response = parse_user_input(messages, message.content)
        except Exception as error:
            await message.channel.send(f"Error: {error}. Please try again.")
            return

    await send_long_message(message.channel, response)

def run_discord_chat():
    if not DISCORD_BOT_TOKEN:
        raise RuntimeError("DISCORD_BOT_TOKEN is not set. Add it to your .env file before running Mosfet.")

    if not DISCORD_ALLOWED_USER_ID:
        raise RuntimeError("DISCORD_ALLOWED_USER_ID is not set. Add your Discord user ID to your .env file before running Mosfet.")

    client.run(DISCORD_BOT_TOKEN)

import discord
from core import parse_user_input, messages
from config import GOODBYE_MESSAGE, DISCORD_BOT_TOKEN, DISCORD_MESSAGE_LIMIT

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

    client.run(DISCORD_BOT_TOKEN)

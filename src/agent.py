from config.client import client
from tools import tools

def agent_ask(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    return completion.choices[0].message.content
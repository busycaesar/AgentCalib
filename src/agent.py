from config.client import client
from tools import tools, call_function
import json

def agent_ask(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    return completion.choices[0].message

def agent_run(messages):
    llm_message = agent_ask(messages)

    if not llm_message.tool_calls:
        return llm_message.content

    for tool_call in llm_message.tool_calls:
        function_name = tool_call.function.name
        function_arguments = json.loads(tool_call.function.arguments)

        messages.append(llm_message)

        result = call_function(function_name, function_arguments)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        )

    response = agent_ask(messages)

    return response.content
from config.client import client
from skill_command import get_skill_content
from tools import tools, call_function
import json

def agent_ask(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    return completion.choices[0].message

def agent_run(messages, user_input):
    skill_content = get_skill_content(user_input)

    if skill_content is not None:
        messages.append({"role": "system", "content": skill_content})

    messages.append({"role": "user", "content": user_input})

    try:
        llm_message = agent_ask(messages)

        if llm_message.tool_calls:
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

            llm_message = agent_ask(messages)

        response = llm_message.content
    except Exception:
        messages.pop()
        if skill_content is not None:
            messages.pop()
        raise

    messages.append({"role": "assistant", "content": response})

    return response
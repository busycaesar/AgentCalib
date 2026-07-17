from config import client, model
from .slash_command import get_skill_content
from tools import tools, call_function
import json
from utils import clean_response

def agent_ask(messages):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )

    return completion.choices[0].message

def parse_user_input(messages, user_input):
    try:
        skill_content = get_skill_content(user_input)

        if skill_content is not None:
            messages.append({"role": "system", "content": skill_content})

        messages.append({"role": "user", "content": user_input})

        response = agent_loop(messages)
       
    except Exception:
        messages.pop()
        if skill_content is not None:
            messages.pop()
        raise

    messages.append({"role": "assistant", "content": response})

    return response
    

def agent_loop(messages):
    while True:
        llm_message = agent_ask(messages)
        
        if not llm_message.tool_calls:
            response = clean_response(llm_message.content)
            break

        messages.append(llm_message)
        for tool_call in llm_message.tool_calls:
            function_name = tool_call.function.name
            function_arguments = json.loads(tool_call.function.arguments)
            result = call_function(function_name, function_arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            )
    
    return response
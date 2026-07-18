from adapters import llm
from .slash_command import get_skill_content
from tools import tools, call_function
import json
from utils import clean_response

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
        llm_message = llm.infer(messages, tools)
        
        if not llm_message.tool_calls:
            content = llm_message.content or ""
            response = clean_response(content)
            break

        messages.append(llm.format_llm_response(llm_message))

        tool_call_results = []

        for tool_call in llm_message.tool_calls:
            function_name = tool_call.function.name
            function_arguments = json.loads(tool_call.function.arguments)
            
            result = call_function(function_name, function_arguments)

            tool_call_results.append((tool_call.id, json.dumps(result)))

        messages.extend(llm.format_tool_call_results(tool_call_results))
    
    return response
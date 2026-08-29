def log_skill_injection(user_input):
    print(f"→ {user_input.split()[0]}: Loaded ")

def log_llm_call(function_name, function_arguments):
    print(f"→ {function_name}({function_arguments}): Calling")

def log_tool_call(name):
    print(f"✓ {name} Done")
from .internal import add_new_skill, browse_internet, get_skill_content

# The list of tools and required arguments, to assist the LLM.
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_new_skill",
            "description": "Add a new skill for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "A short, filesystem-safe identifier for the skill, used directly as the filename. Use snake_case, capped at 2 words, unless the user explicitly specifies a different name."
                    },
                    "description": {"type": "string"},
                    "content": { "type": "string" },
                },
                "required": ["name", "description", "content"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_skill_content",
            "description": "Load the full instructions for one of your available skills by name, so you can follow them.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Exact skill name from your available skills list."}
                },
                "required": ["name"],
                "additionalProperties": False,
            },  
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browse_internet",
            "description": "Browse the internet to get the latest and updated information to be able to better serve the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True
        }
    }
]

def call_function(name, args):
    if name == "add_new_skill":
        return add_new_skill(**args)
    elif name == "get_skill_content":
        return get_skill_content(**args)
    elif name == "browse_internet":
        return browse_internet(**args)
    else:
        return f"No tool available with name {name}."
from .internal import create_skill, browse_internet

# The list of tools and required arguments, to assist the LLM.
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_skill",
            "description": "Create a new skill file for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_content": {"type": "string"},
                    "skill_name": {"type": "string"},
                },
                "required": ["skill_content", "skill_name"],
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
    if name == "create_skill":
        return create_skill(**args)
    elif name == "browse_internet":
        return browse_internet(**args)
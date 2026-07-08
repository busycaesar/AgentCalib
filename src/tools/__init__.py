from src.tools.create_skill import create_skill

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
    }
]

def call_function(name, args):
    if name == "create_skill":
        return create_skill(**args)
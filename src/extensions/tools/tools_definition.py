# The list of tools and required arguments, to assist the LLM.
tools = [
    {
        "type": "function",
        "function": {
            "name": "int_add_new_skill",
            "description": "Add a new skill for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "A short, filesystem-safe identifier for the skill, used directly as the filename. Use snake_case, capped at 2 words, unless the user explicitly specifies a different name."
                    },
                    "description": {
                        "type": "string",
                        "description": "A one-line summary of what the skill does and when to use it, shown in the skills index."
                    },
                    "content": {
                        "type": "string",
                        "description": "The full skill instructions in Markdown — the body the agent follows when the skill is invoked."
                    },
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
            "name": "int_get_skill_content",
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
            "name": "int_web_search_tool",
            "description": "Search the web for a query and get back page titles, URLs, and short snippets. Use this to find sources before fetching their full content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "int_fetch_content_from_url",
            "description": "Fetch and read the content of a specific URL, typically one found via the web search tool. Returns the page's main content as clean text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to fetch."} 
                },
                "required": ["url"],
                "additionalProperties": False,
            },
            "strict": True
        }
    }
]
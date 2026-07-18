from config import messages
from utils import get_skills_list

available_skills = get_skills_list()

if available_skills:
    messages.append({
        "role": "system",
        "content": f"You have the following skills available. When a skill fits the request, use the tool that loads a skill's full instructions by name, then follow them:\n{available_skills}."
    })
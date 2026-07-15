from config import messages
from utils import get_skills_list

available_skills = get_skills_list()

if available_skills:
    messages.append({
        "role": "system",
        "content": f"You have the following skills available. Call load_skill with the exact name to load one's full instructions before using it:\n{available_skills}"
    })
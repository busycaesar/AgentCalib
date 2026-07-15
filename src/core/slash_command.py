from utils.skills import get_skill_by_name

def get_skill_content(user_input):
    if not user_input.startswith("/"):
        return None

    parts = user_input[1:].split(maxsplit=1)

    if not parts:
        return None

    return get_skill_by_name(parts[0])
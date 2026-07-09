from config.paths import SKILLS_DIR


def get_skill_content(user_input):
    if not user_input.startswith("/"):
        return None

    parts = user_input[1:].split(maxsplit=1)

    if not parts:
        return None

    skill_path = SKILLS_DIR / f"{parts[0]}.md"

    if not skill_path.is_file():
        return None

    return skill_path.read_text()
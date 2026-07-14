from config.paths import SKILLS_DIR
from utils.skills import build_skill_file

def create_skill(name, description, content):
    name = name.lower().replace(" ", "_")

    skill_path = SKILLS_DIR / f"{name}.md"

    with open(skill_path, "w") as file:
        skill_file_content = build_skill_file(description, content)
        file.write(skill_file_content)

def browse_internet(query):
    return "Result"
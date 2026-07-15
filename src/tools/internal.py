from config.paths import SKILLS_DIR
from utils.skills import build_skill_file, update_skills_index, get_skill_by_name

def create_new_skill(name, description, content):
    name = name.lower().replace(" ", "_")

    skill_path = SKILLS_DIR / f"{name}.md"

    with open(skill_path, "w") as file:
        skill_file_content = build_skill_file(description, content)
        file.write(skill_file_content)

def add_new_skill(name, description, content):
    create_new_skill(name, description, content)
    update_skills_index(name, description)

def get_skill_content(name):
    print("Agent Using Skill.", name)

    content = get_skill_by_name(name)

    if not content:
        return "No skill"
    
    return content

def browse_internet(query):
    return "Result"
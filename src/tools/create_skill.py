from config.paths import SKILLS_DIR

def create_skill(skill_content, skill_name):
    skill_path = SKILLS_DIR / f"{skill_name}.md"

    with open(skill_path, "w") as file:
        file.write(skill_content)
from config.paths import SKILLS_DIR

def create_skill(name, description, content):
    skill_path = SKILLS_DIR / f"{name}.md"

    with open(skill_path, "w") as file:
        file.write(f"description: {description}\n---\n{content}")

def browse_internet(query):
    return "Result"
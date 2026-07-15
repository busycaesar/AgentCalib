from config.paths import SKILLS_DIR
import json

DELIMITER = "---"
SKILLS_INDEX_PATH = SKILLS_DIR / "index.json"

def build_skill_file(description, content):
    return f"""\
{DELIMITER}
description: {description}
{DELIMITER}

{content}
"""

def get_skills_list():
    if not SKILLS_INDEX_PATH.is_file():
        return {}

    content = SKILLS_INDEX_PATH.read_text().strip()

    if not content:
        return {}

    return json.loads(content)

def get_skill_by_name(name):
    skill_path = SKILLS_DIR / f"{name}.md"

    if not skill_path.is_file():
        return None

    return skill_path.read_text()

def update_skills_index(name, description):
    index = get_skills_list()
    index[name] = description

    SKILLS_INDEX_PATH.write_text(json.dumps(index, indent=2))


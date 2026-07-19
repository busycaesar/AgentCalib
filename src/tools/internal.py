from config import SKILLS_DIR
from utils import build_skill_file, update_skills_index, get_skill_by_name
from adapters import web_search
import trafilatura

def create_new_skill(name, description, content):
    if not name or not name.strip():
        return "Error: skill name must not be empty."
    if not description or not description.strip():
        return "Error: skill description must not be empty."
    if not content or not content.strip():
        return "Error: skill content must not be empty."

    name = name.lower().replace(" ", "_")

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    skill_path = SKILLS_DIR / f"{name}.md"

    with open(skill_path, "w") as file:
        skill_file_content = build_skill_file(description, content)
        file.write(skill_file_content)

def add_new_skill(name, description, content):
    error = create_new_skill(name, description, content)
    if error:
        return error

    update_skills_index(name, description)

# If the name of the following function is changed, make sure to update the name in core/build_initial_message.py as well.
def get_skill_content(name):
    content = get_skill_by_name(name)

    if not content:
        return f"No skill available with name {name}."
    
    return content

def web_search_tool(query):
    return web_search.search(query)

def fetch_content_from_url(url):
    downloaded = trafilatura.fetch_url(url)

    if downloaded is None:
        return f"Could not fetch content from {url}."
    
    content = trafilatura.extract(downloaded)

    if not content:
        return f"No readable content found at {url}."

    return content
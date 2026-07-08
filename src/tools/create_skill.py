def create_skill(skill_content, skill_name):
    """
    Create a new skill.
    """

    with open(f'{skill_name}.md', 'w') as file:
        file.write(skill_content)
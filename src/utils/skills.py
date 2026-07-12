DELIMITER = "---"

def build_skill_file(description, content):
    return f"""\
            {DELIMITER}
            description: {description}
            {DELIMITER}

            {content}
            """
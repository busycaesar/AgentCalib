def clean_response(content):
    # Some models wrap their whole reply in a pseudo-tag, e.g. "<hello />".
    # Strip a single leading "<" and/or trailing "/>" wrapper if present.
    if not content:
        return content

    cleaned = content.strip()

    if cleaned.startswith("<"):
        cleaned = cleaned[1:]
    if cleaned.endswith("/>"):
        cleaned = cleaned[:-2]

    return cleaned.strip()
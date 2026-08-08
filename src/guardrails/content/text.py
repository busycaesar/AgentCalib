def extract_text(content):
    """
    Normalizes message content into plain text for the checkers. Content is usually a string, but provider-formatted messages (e.g. Anthropic tool results) can be a list of content blocks instead.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            str(block.get("content", block)) if isinstance(block, dict) else str(block)
            for block in content
        )

    return ""

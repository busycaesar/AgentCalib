import re

PII_PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
}

# Banned words/phrases
BLOCKLIST = []

def run(text):
    """
    Rule-based checker. Returns a list of violation labels, or [] if clean.
    """
    violations = [f"pii:{label}" for label, pattern in PII_PATTERNS.items() if pattern.search(text)]

    # Only need lowered text to check the words from the blocklist.
    lowered_text = text.lower()

    violations += [f"blocklist:{word}" for word in BLOCKLIST if word.lower() in lowered_text]

    return violations
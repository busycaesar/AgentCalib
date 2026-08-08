from .rules import run as rules_run
from .judge import run as judge_run
from .text import extract_text

# Every check we run on a message, one after another. Each one looks at the text and hands back a list of problems it found (empty if it found none). To turn on a new kind of check later, just add its function here.
CHECKERS = [rules_run, judge_run]

# Class to raise exception whenever the guardrails detect an issue.
class GuardrailViolation(Exception):
    def __init__(self, direction, violations):
        self.direction = direction
        self.violations = violations
        super().__init__(f"Guardrail violation ({direction}): {', '.join(violations)}")

def enforce(content, direction):
    # Parse the text to ensure that its always a string.
    text = extract_text(content)

    violations = []

    for checker in CHECKERS:
        violations.extend(checker(text))

        # A cheaper checker (like the regex rules) already found a problem —
        # skip the rest, so we don't waste a judge model call on text we're
        # about to reject anyway.
        if violations:
            break

    # Raise exception when there is a violation.
    if violations:
        raise GuardrailViolation(direction, violations)
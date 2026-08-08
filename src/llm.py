from adapters import llm as raw_llm
from guardrails import GuardedLLM

llm = GuardedLLM(raw_llm)
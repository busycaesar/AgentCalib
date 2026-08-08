from .hub import enforce

class GuardedLLM:
    def __init__(self, provider):
        self.provider = provider

    def infer(self, messages, tools):
        # Only get the content of the last message in the messages array.
        enforce(messages[-1]["content"], direction="input")

        response = self.provider.infer(messages, tools)

        if response.content:
            enforce(response.content, direction="output")

        return response

    # Pass the implementation directly to the provider methods.

    def format_llm_response(self, generated_response):
        return self.provider.format_llm_response(generated_response)

    def format_tool_call_results(self, tool_call_results):
        return self.provider.format_tool_call_results(tool_call_results)
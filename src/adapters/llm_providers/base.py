from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def infer(self, messages, tools):
        """
        Send messages and the list of tools to the LLM to received the generated response or a tool to be called.
        """

    @abstractmethod
    def format_llm_response(self, generated_response):
        """
        Format the generated response by the model to append in the messages array.
        """

    @abstractmethod
    def format_tool_call_results(self, tool_call_results):
        """
        Format the result returned by the called tool into the messages array.
        """
from abc import ABC, abstractmethod

class WebSearchProvider(ABC):
    @abstractmethod
    def search(self, query):
        """
        Search the web for the given query and return the list of title, url and snippet.
        """
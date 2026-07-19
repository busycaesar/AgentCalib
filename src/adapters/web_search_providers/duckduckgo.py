from .base import WebSearchProvider
from ddgs import DDGS

class DuckDuckGoWebSearch(WebSearchProvider):
    def __init__(self, max_results):
        self.max_results = max_results

    def search(self, query):
        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results = self.max_results
            )

        return self._format_search_results(search_results)

    def _format_search_results(self, search_results):
        return [
            {
                "title": search_result["title"],
                "url": search_result["href"],
                "snippet": search_result["body"]
            }
            for search_result in search_results
        ]
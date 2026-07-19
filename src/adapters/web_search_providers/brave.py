from .base import WebSearchProvider
import httpx

BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

class BraveWebSearch(WebSearchProvider):
    def __init__(self, api_key, max_results):
        self.api_key = api_key
        self.max_results = max_results

    def search(self, query):
        # Using httpx because its already pulle in as a dependency of OpenAI and Anthropic SDK.
        response = httpx.get(
            BRAVE_SEARCH_URL,
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": self.api_key
            },
            params={
                "q": query,
                "count": self.max_results
            }
        )

        # Checks the status code of the response. Raises exception if its error.
        response.raise_for_status()

        # Gets the results from web.results from the response object.
        # Includes a fallback value for both web as well as results.
        search_results = response.json().get("web", {}).get("results", [])

        return self._format_search_results(search_results)

    def _format_search_results(self, search_results):
        return [
            {
                "title": search_result["title"],
                "url": search_result["url"],
                "snippet": search_result["description"]
            }
            for search_result in search_results
        ]

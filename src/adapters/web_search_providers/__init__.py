from config import WEB_SEARCH_PROVIDER, WEB_SEARCH_MAX_RESULTS, BRAVE_API_KEY
from .duckduckgo import DuckDuckGoWebSearch
from .brave import BraveWebSearch

if WEB_SEARCH_PROVIDER == "Brave":
    if not BRAVE_API_KEY:
        raise RuntimeError("BRAVE_API_KEY is not set. Set it in .env before running Mosfet.")

    web_search = BraveWebSearch(BRAVE_API_KEY, WEB_SEARCH_MAX_RESULTS)
else:
    # Default to Duck Duck Go if the Web Search Provider is not customized because DDG does not need any API.
    web_search = DuckDuckGoWebSearch(WEB_SEARCH_MAX_RESULTS)
import os
from dotenv import load_dotenv
from config import WEB_SEARCH_PROVIDER, WEB_SEARCH_MAX_RESULTS
from .duckduckgo import DuckDuckGoWebSearch
from .brave import BraveWebSearch

load_dotenv()

if WEB_SEARCH_PROVIDER == "Brave":
    api_key = os.getenv("BRAVE_API_KEY")

    if not api_key:
        raise RuntimeError("BRAVE_API_KEY is not set. Set it in .env before running Mosfet.")

    web_search = BraveWebSearch(api_key, WEB_SEARCH_MAX_RESULTS)
else:
    # Default to Duck Duck Go if the Web Search Provider is not customized because DDG does not need any API.
    web_search = DuckDuckGoWebSearch(WEB_SEARCH_MAX_RESULTS)
from config import WEB_SEARCH_PROVIDER, MAX_RESULTS
from .duckduckgo import DuckDuckGoWebSearch

# Default to Duck Duck Go if the Web Search Provider is not customized because DDG does not need any API.
web_search = DuckDuckGoWebSearch(MAX_RESULTS)
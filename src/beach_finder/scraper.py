"""Deterministic scraping layer.

Job: turn a source page (e.g. ebf.li) into a list of validated Tournament
objects. No LLM here — this is deterministic parsing. If some listings are
too messy to parse deterministically, an LLM *fallback* (structured
extraction) can rescue the long tail later — but get the deterministic path
working first.
"""

from beach_finder.models import Tournament


def fetch_tournaments(source_url: str) -> list[Tournament]:
    """Fetch and parse tournaments from a source URL.

    TODO:
      1. Request the page (requests).
      2. Before scraping HTML, check whether the site exposes a JSON
         endpoint (open DevTools → Network) — that's far cleaner and more
         stable than parsing markup.
      3. Otherwise parse the HTML (BeautifulSoup).
      4. Build and return a list of validated Tournament objects.
    """
    raise NotImplementedError

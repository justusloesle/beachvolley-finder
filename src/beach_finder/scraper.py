"""Deterministic scraping layer.

Job: turn a source page (e.g. ebf.li) into a list of validated Tournament
objects. No LLM here — this is deterministic parsing. If some listings are
too messy to parse deterministically, an LLM *fallback* (structured
extraction) can rescue the long tail later — but get the deterministic path
working first.
"""
import uuid

from beach_finder.models import Tournament
import requests
from datetime import date, datetime

BASE_URL = "https://www.ebf.li/api/v1/tournaments/"
def fetch_page(url: str, req_params: dict):
    resp = requests.get(
        url,
        params= req_params,
        headers= {"User-Agent": "beach-volley-finder"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

    return data


def fetch_tournaments() -> list[Tournament]:
    """Fetch and parse tournaments from a source URL.

    TODO:
      1. Request the page (requests).
      2. Before scraping HTML, check whether the site exposes a JSON
         endpoint (open DevTools → Network) — that's far cleaner and more
         stable than parsing markup.
      3. Otherwise parse the HTML (BeautifulSoup).
      4. Build and return a list of validated Tournament objects.
    """
    tournaments = []
    num_of_tournaments = 0

    url = BASE_URL

    params = {
        "is_open": "1",
        "tags": "life-is-a-beach-tour",
        "details": "1",
    }
    while url is not None:
        data = fetch_page(url, params)
        num_of_tournaments = data["count"]
        results = data["results"]
        params = None
        for result in results:
            tournament = _to_tournament(result)
            tournaments.append(tournament)

        url = data["next"]

    if num_of_tournaments != len(tournaments):
        print(f"WARNING: got {len(tournaments)}, expected {data['count']}")

    return tournaments





def _to_tournament(raw: dict):

    tournament_id = raw["id"]
    name: str = raw["name"]["de"]
    location: str =  raw["venue"]["city"]
    tournament_date: date = raw["date"]
    begin_time: datetime = raw["begin"]

    latitude: float = raw["venue"]["latitude"]
    longitude: float = raw["venue"]["longitude"]

    level: str = raw["level"]["de"]
    team_mode: str = raw["teamMode"]["name"]
    registration_url: str = raw["url"]

    tournament_dict = {
        "id" : tournament_id,
        "name" : name,
        "location" : location,
        "tournament_date" : tournament_date,
        "begin_time" : begin_time,
        "latitude" : latitude,
        "longitude" : longitude,
        "level" : level,
        "team_mode" : team_mode,
        "registration_url" : registration_url
    }

    return Tournament.model_validate(tournament_dict)


if __name__ == "__main__":
   tournaments = fetch_tournaments()
   print(tournaments)



from beach_finder.models import Tournament, RankingResult, RankingList
from beach_finder.scraper import fetch_tournaments
from beach_finder.geo import filter_by_distance
from beach_finder.ranker import filter_by_mode, rank_tournaments
from random import randint


def find_tournaments(max_km: int, preferences: str, modes: list[str]) -> list[Tournament]:
    raw = fetch_tournaments()
    filtered = filter_by_distance(raw, max_km)
    #stubbed travel time geo function to test LLM layer - to be removed later
    for tournament in filtered:
        tournament.estimated_travel_time = randint(20, 200)
    allowed = filter_by_mode(filtered, modes)
    ranked = rank_tournaments(allowed, preferences)
    return ranked

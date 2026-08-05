

from beach_finder.models import TournamentCandidate, User, Tournament
from beach_finder.scraper import fetch_tournaments
from beach_finder.geo import filter_by_distance
from beach_finder.ranker import filter_by_mode, rank_tournaments
from random import randint


def find_tournaments_single_user(raw: list[Tournament], user: User) -> list[TournamentCandidate]:

    candidates = filter_by_distance(raw, user)
    #stubbed travel time geo function to test LLM layer - to be removed later
    for candidate in candidates:
        candidate.estimated_travel_time = randint(20, 200)
    allowed = filter_by_mode(candidates, user)
    ranked = rank_tournaments(allowed, user)
    return ranked


def find_tournament_workflow(users: list[User]):
    raw = fetch_tournaments()
    for user in users:
        find_tournaments_single_user(raw, user)
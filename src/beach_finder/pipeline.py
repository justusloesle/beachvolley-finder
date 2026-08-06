

from beach_finder.models import TournamentCandidate, User, Tournament
from beach_finder.scraper import fetch_tournaments
from beach_finder.geo import filter_by_distance
from beach_finder.ranker import filter_by_mode,filter_by_level, rank_tournaments
from beach_finder.notifier import send_message, format_message_response
from random import randint


def find_tournaments_single_user(raw: list[Tournament], user: User) -> None:

    candidates = filter_by_distance(raw, user)
    #stubbed travel time geo function to test LLM layer - to be removed later
    for candidate in candidates:
        candidate.estimated_travel_time = randint(20, 200)
    modes = filter_by_mode(candidates, user)
    levels = filter_by_level(modes, user)
    ranked = rank_tournaments(levels, user)
    message: str = format_message_response(ranked)
    send_message(message, user)




def find_tournament_workflow(users: list[User]):
    raw = fetch_tournaments()
    for user in users:
        find_tournaments_single_user(raw, user)
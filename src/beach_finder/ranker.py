"""AI layer — the LLM's ONLY job.

Input:  structured facts (a Tournament plus its transit facts from geo.py)
        and your soft preferences in natural language.
Output: a ranking + a human-readable justification.

The LLM does NOT compute travel times or distances — those are facts from
the deterministic layers. It does the fuzzy multi-criteria tradeoff and the
summary. That boundary is the whole point of the project and the thing you
want to be able to defend in the interview.
"""

from beach_finder.models import TournamentCandidate, RankingResult, RankingList, User
from google import genai
from beach_finder.config import ANTHROPIC_API_KEY


def filter_by_mode(
    candidates: list[TournamentCandidate],
    user: User) -> list[TournamentCandidate]:
    allowed_modes = {m.lower() for m in user.team_modes}
    filtered = []
    for candidate in candidates:
        if candidate.tournament.team_mode.lower() in allowed_modes:
            filtered.append(candidate)

    return filtered

def filter_by_level(
        candidates: list[TournamentCandidate],
        user: User) -> list[TournamentCandidate]:
    allowed_levels = {l.lower() for l in user.levels}
    filtered = []
    for candidate in candidates:
        if candidate.tournament.level.lower() in allowed_levels:
            filtered.append(candidate)

    return filtered

def rank_tournaments(
    candidates: list[TournamentCandidate],
    user: User,
) -> list[TournamentCandidate]:
    """Rank tournaments using the LLM as a judgment layer.

    TODO:
      - assemble a prompt from the structured facts + `preferences`
      - ask the LLM for a ranking + short reasoning per tournament
      - use a pydantic model for the LLM's structured output so you get
        typed results back, not a text blob you have to regex
      - later: a tiny eval — compare the LLM ranking against a handful you
        ranked yourself, and record the agreement rate in the README
    """
    prompt: str = "You are specialized in ranking beach-volleyball tournaments. You are given a list of tournaments, each with a unique id, distance to Garching, a mode, level, estimated travel time, and a starting time. These are facts, do not question or recalculate them. \n "
    prompt += _serialize_tournaments(candidates)
    prompt += f"Furthermore, you are given the following general user preferences {user.preferences} \n"
    prompt += "Evaluate and rank the tournaments based on the given data, primarily take into account travel time, but weigh in the preferences regarding the other data equally."




    client = genai.Client(api_key=ANTHROPIC_API_KEY)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": RankingList,
            "temperature": 0.3

        },
    )

    parsed= response.parsed
    if not isinstance(parsed, RankingList):
        raise ValueError(f"unexpected LLM output: {response.text}")


    by_id = {c.tournament.id: c for c in candidates}
    ranked = []
    for r in parsed.rankings:
        candidate = by_id.get(r.id)
        if candidate is not None:
            candidate.reasoning = r.reasoning
            candidate.rank = r.rank
            ranked.append(candidate)

    ranked.sort(key=lambda c: c.rank)
    return ranked

def _serialize_tournaments(candidates: list[TournamentCandidate]) -> str:
    serialized: str = ""
    for candidate in candidates:
        t = candidate.tournament
        serialized += f" Tournament {t.name} with id {t.id}, distance: {candidate.distance}, mode: {t.team_mode}, level: {t.level}, travel duration: {candidate.estimated_travel_time}, starting time: {t.begin_time} \n"

    return serialized
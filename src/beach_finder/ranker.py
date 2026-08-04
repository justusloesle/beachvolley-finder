"""AI layer — the LLM's ONLY job.

Input:  structured facts (a Tournament plus its transit facts from geo.py)
        and your soft preferences in natural language.
Output: a ranking + a human-readable justification.

The LLM does NOT compute travel times or distances — those are facts from
the deterministic layers. It does the fuzzy multi-criteria tradeoff and the
summary. That boundary is the whole point of the project and the thing you
want to be able to defend in the interview.
"""

from beach_finder.models import Tournament, RankingResult, RankingList
from google import genai
from beach_finder.config import GEMINI_API_KEY

def filter_by_mode(
    tournaments: list[Tournament],
    modes: list[str]) -> list[Tournament]:
    filtered = []
    for tournament in tournaments:
        if tournament.team_mode in modes:
            filtered.append(tournament)

    return filtered


def rank_tournaments(
    tournaments: list[Tournament],
    preferences: str,
) -> list[Tournament]:
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
    prompt += _serialize_tournaments(tournaments)
    prompt += f"Furthermore, you are given the following general user preferences {preferences} \n"
    prompt += "Evaluate and rank the tournaments based on the given data, primarily take into account travel time, but weigh in the preferences regarding the other data equally."




    client = genai.Client(api_key=GEMINI_API_KEY)

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


    by_id = {t.id: t for t in tournaments}
    ranked = []
    for r in parsed.rankings:
        t = by_id.get(r.id)
        if t is not None:
            t.reasoning = r.reasoning
            ranked.append(t)
    return ranked

def _serialize_tournaments(tournaments: list[Tournament]) -> str:
    serialized: str = ""
    for tournament in tournaments:
        serialized += f" Tournament {tournament.name} with id {tournament.id}, distance: {tournament.distance}, mode: {tournament.team_mode}, level: {tournament.level}, travel duration: {tournament.estimated_travel_time}, starting time: {tournament.begin_time} \n"

    return serialized
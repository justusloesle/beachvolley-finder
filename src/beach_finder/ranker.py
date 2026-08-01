"""AI layer — the LLM's ONLY job.

Input:  structured facts (a Tournament plus its transit facts from geo.py)
        and your soft preferences in natural language.
Output: a ranking + a human-readable justification.

The LLM does NOT compute travel times or distances — those are facts from
the deterministic layers. It does the fuzzy multi-criteria tradeoff and the
summary. That boundary is the whole point of the project and the thing you
want to be able to defend in the interview.
"""

from beach_finder.models import Tournament


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
    raise NotImplementedError

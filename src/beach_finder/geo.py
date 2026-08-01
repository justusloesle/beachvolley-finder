"""Deterministic geo layer: distance filtering and transit facts.

Distances, transit times and transfer counts are HARD FACTS. They come from
the Maps/Directions API — never from the LLM. Keep this layer purely
deterministic and easy to test.
"""

from beach_finder.models import Tournament


def filter_by_distance(
    tournaments: list[Tournament],
    origin: str,
    max_km: float,
) -> list[Tournament]:
    """Return only tournaments within `max_km` of `origin`.

    TODO:
      - geocode the origin and each tournament location
      - compute the distance
      - keep those within max_km

    Tip: this is a pure function, so it's the easiest thing in the whole
    project to unit-test first. Start here to get comfortable with pytest.
    """
    raise NotImplementedError

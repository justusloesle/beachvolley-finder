"""Manual smoke test for the AI ranking layer.

Run with:  uv run python scripts/try_ranker.py

Uses the shared test fixtures plus HAND-MADE transit numbers, so the ranker
can be developed before the Routes API is wired up. When the real transit
layer lands, only the numbers below change — the ranker stays untouched.
"""

from beach_finder.ranker import rank_tournaments
from tests.fixtures import GERMERING, NUERNBERG, OBERURSEL

# Fake transit facts, in minutes. Deliberately set up so the ranking is a
# real tradeoff and not just "closest wins":
#   - Germering  : near, but awkward connection
#   - Nuernberg  : further, but a fast direct train
#   - Oberursel  : far and slow, should lose
FAKE_TRAVEL_MINUTES = {
    "Germering": 55,
    "Nürnberg": 75,
    "Oberursel": 210,
}

FAKE_DISTANCE_KM = {
    "Germering": 25.0,
    "Nürnberg": 135.0,
    "Oberursel": 300.0,
}

PREFERENCES = (
    "Ich spiele Herren oder Mixed, kein Damen-Turnier. "
    "Frühe Startzeiten sind okay, aber ich hasse enge Umstiege am Morgen — "
    "lieber etwas länger unterwegs als hektisch. "
    "Level basic oder freestyle bevorzugt."
)


def main() -> None:
    tournaments = [ NUERNBERG, GERMERING, OBERURSEL]

    # Fill in the facts the deterministic layers would normally provide.
    for t in tournaments:
        t.distance = FAKE_DISTANCE_KM[t.location]
        t.estimated_travel_time = FAKE_TRAVEL_MINUTES[t.location]

    print("=== INPUT ===")
    for t in tournaments:
        print(f"  {t.name} | {t.distance} km | {t.estimated_travel_time} min")

    print("\n=== RANKING ===")
    ranked = rank_tournaments(tournaments, PREFERENCES)

    for i, t in enumerate(ranked, start=1):
        print(f"  {i}. {t.name} ({t.location})")
        print(t.reasoning)


if __name__ == "__main__":
    main()
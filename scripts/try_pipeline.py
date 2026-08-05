

from beach_finder.pipeline import find_tournaments
from beach_finder.users import JUSTUS


def main() -> None:

    ranked = find_tournaments(JUSTUS)

    for i, candidate in enumerate(ranked, start=1):
        t = candidate.tournament
        print(f"  {i}. {t.name} ({t.tournament_date}) ({t.location})")
        print(candidate.reasoning)

if __name__ == "__main__":
    main()
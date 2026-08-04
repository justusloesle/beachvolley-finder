

from beach_finder.pipeline import find_tournaments
MAX_KM = 100
PREFERENCES = "I prefer mixed and Herren tournaments, level: basic > freestyle > expert."
MODES = ["Herren", "Mixed"]

def main() -> None:

    ranked = find_tournaments(MAX_KM, PREFERENCES, MODES)

    for i, t in enumerate(ranked, start=1):
        print(f"  {i}. {t.name} ({t.tournament_date}) ({t.location})")
        print(t.reasoning)

if __name__ == "__main__":
    main()
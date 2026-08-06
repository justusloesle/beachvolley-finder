

from beach_finder.pipeline import find_tournaments_single_user
from beach_finder.scraper import fetch_tournaments
from beach_finder.users import JUSTUS


def main() -> None:
    raw = fetch_tournaments()
    find_tournaments_single_user(raw, JUSTUS)


if __name__ == "__main__":
    main()
from beach_finder.pipeline import find_tournaments_workflow
from beach_finder.users import USERS



def main() -> None:
    find_tournaments_workflow(USERS)



if __name__ == "__main__":
    main()

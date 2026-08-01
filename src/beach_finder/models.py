

from pydantic import BaseModel
from pydantic import field_validator
from datetime import date, datetime



class Tournament(BaseModel):
    """A single tournament parsed from a source like ebf.li.
    """




    name: str
    location: str
    tournament_date: date
    begin_time: datetime

    latitude: float | None = None
    longitude: float | None = None

    level: str
    team_mode: str

    taken_spots: int
    max_spots: int
    registration_url: str | None = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, tournament_date: date) -> date:
        if tournament_date < date.today():
            raise ValueError(f"date is in the past: {tournament_date}")
        return tournament_date


    @field_validator("taken_spots")
    @classmethod
    def validate_taken_spots(cls, taken: int, max_slots: int) -> int:
        if taken > max_slots - 2:
            raise ValueError(f"tournament is full: {taken} slots of {max_slots} taken")
        return taken

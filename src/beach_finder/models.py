import uuid

from pydantic import BaseModel, Field
from pydantic import field_validator
from datetime import date, datetime



class Tournament(BaseModel):
    """A single tournament parsed from a source like ebf.li.
    """



    id: int
    name: str
    location: str
    tournament_date: date
    begin_time: datetime

    latitude: float | None = None
    longitude: float | None = None


    level: str
    team_mode: str

    distance: float | None = None

    estimated_travel_time: int | None = None

    reasoning: str | None = None
    rank: int | None = None

#spot-logic may (not) be needed because of query parameters
   # taken_spots: int
   # max_spots: int
    registration_url: str | None = None

    @field_validator("tournament_date")
    @classmethod
    def validate_date(cls, tournament_date: date) -> date:
        if tournament_date < date.today():
            raise ValueError(f"date is in the past: {tournament_date}")
        return tournament_date

class RankingResult(BaseModel):
    """The structure of the result-format of the LLM"""
    rank:int
    id: int
    reasoning:str = Field(description="One or two sentences explaining this ranking, mentioning the concrete tradeoff")

class RankingList(BaseModel):
    rankings: list[RankingResult]




"""
@field_validator("taken_spots")
    @classmethod
    def validate_taken_spots(cls, taken: int, max_slots: int) -> int:
        if taken > max_slots - 2:
            raise ValueError(f"tournament is full: {taken} slots of {max_slots} taken")
        return taken
"""


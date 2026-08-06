import uuid

from pydantic import BaseModel, Field
from pydantic import field_validator
from datetime import date, datetime



class Tournament(BaseModel):
    """A single tournament parsed from a source like ebf.li.

    Facts only: everything here comes from the source and is identical for
    every user. Anything the pipeline *derives* for one particular user —
    distance, travel time, the LLM's ranking — belongs on
    TournamentCandidate, so one scraped list can be shared across users
    without runs leaking state into each other.
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

    registration_url: str | None = None

    @field_validator("tournament_date")
    @classmethod
    def validate_date(cls, tournament_date: date) -> date:
        if tournament_date < date.today():
            raise ValueError(f"date is in the past: {tournament_date}")
        return tournament_date


class TournamentCandidate(BaseModel):
    """A tournament as it looks *for one user*.

    Wraps the shared Tournament facts and collects the per-user values the
    pipeline fills in as it goes: `distance` at the geo stage,
    `estimated_travel_time` at the transit stage, `reasoning` and `rank` at
    the LLM stage.
    """

    tournament: Tournament
    distance: float

    estimated_travel_time: int | None = None

    reasoning: str | None = None
    rank: int | None = None

class RankingResult(BaseModel):
    """The structure of the result-format of the LLM"""
    rank:int
    id: int
    reasoning:str = Field(description="One sentence explaining this ranking, mentioning the concrete tradeoff (german)")

class RankingList(BaseModel):
    rankings: list[RankingResult]


class User(BaseModel):
    id: str
    max_km: int
    team_modes: list[str]
    levels: list[str]
    preferences: str
    telegram_chat_id: str


"""
@field_validator("taken_spots")
    @classmethod
    def validate_taken_spots(cls, taken: int, max_slots: int) -> int:
        if taken > max_slots - 2:
            raise ValueError(f"tournament is full: {taken} slots of {max_slots} taken")
        return taken
"""


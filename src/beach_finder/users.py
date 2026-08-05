"""Simple multi-user model with user preferences  stored as User-objects"""


from beach_finder.models import User
from uuid import uuid4



JUSTUS = User(
    id= "justus",
    max_km= 100,
    team_modes= ["Herren", "Mixed"],
    preferences= "Preferred: Sundowners and early morning tournaments, shorter travel times as well as levels of basic > freestyle > e-b-f above everything else.",
    telegram_url= ""
)

MAYA = User(
    id= "maya",
    max_km=50,
    team_modes= ["Damen", "Mixed"],
    preferences= "Preferred: Shortest distance and travel time, levels of basic > e-b-f > freestyle above everything else, mixed > damen.",
    telegram_url= ""
)

USERS = [JUSTUS, MAYA]
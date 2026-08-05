"""Deterministic geo layer: distance filtering and transit facts.

Distances, transit times and transfer counts are HARD FACTS. They come from
the Maps/Directions API — never from the LLM. Keep this layer purely
deterministic and easy to test.
"""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import geopy.distance
import requests

from beach_finder.config import GOOGLE_MAPS_API_KEY
from beach_finder.models import Tournament, TournamentCandidate, User
from geopy.distance import distance

LAT_GARCHING = 48.25716781616211
LONG_GARCHING = 11.655027389526367

MAPS_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

# Tournament dates/times are naive; they refer to local German wall-clock time.
LOCAL_TZ = ZoneInfo("Europe/Berlin")

def filter_by_distance(
    tournaments: list[Tournament],
    user: User
) -> list[TournamentCandidate]:
    """Return candidates for the tournaments within `user.max_km` of the origin.

    Pure: the incoming Tournament objects are never written to, so the same
    scraped list can be passed through this function once per user.

    TODO:
      - geocode the origin and each tournament location
      - keep those within max_km

    Tip: this is a pure function, so it's the easiest thing in the whole
    project to unit-test first. Start here to get comfortable with pytest.
    """

    candidates: list[TournamentCandidate] = []

    for tournament in tournaments:
        dist: float = geopy.distance.distance((tournament.latitude, tournament.longitude), (LAT_GARCHING, LONG_GARCHING)).km
        if dist <= user.max_km:
            candidates.append(TournamentCandidate(tournament=tournament, distance=dist))


    candidates.sort(key=lambda c: c.distance)
    return candidates


def set_travel_time(candidates: list[TournamentCandidate]):

    headers = {
            "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
            "X-Goog-FieldMask": "...",
    }

    body = {
        "origin": {"location": {"latLng": {"latitude": ..., "longitude": ...}}},
        "destination": {"location": {"latLng": {"latitude": ..., "longitude": ...}}},
        "travelMode": "TRANSIT",
        "arrivalTime": "...",
        "computeAlternativeRoutes": True,
        "transitPreferences": {
            "routingPreference": "FEWER_TRANSFERS",
            "allowedTravelModes": ["BUS", "SUBWAY", "TRAIN", "LIGHT_RAIL", "RAIL"],
        },
    }



    resp = requests.post(MAPS_URL, json=body, headers=headers, timeout=10)


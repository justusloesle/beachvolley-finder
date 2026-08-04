"""Shared sample tournaments, reusable across test modules.

Coordinates and names are taken from real ebf.li data so the numbers mean
something. Dates are generated relative to today, because the Tournament
model rejects dates in the past — hard-coded dates would silently start
failing once they age.

Import from other test modules with:
    from tests.fixtures import GERMERING, NUERNBERG, OBERURSEL, ALL_TOURNAMENTS
"""

from datetime import date, datetime, timedelta, timezone

from beach_finder.models import Tournament

# Origin used by the distance filter (TUM Garching).
GARCHING = (48.249, 11.651)

_BERLIN_TZ = timezone(timedelta(hours=2))


def _future(days: int, hour: int = 9) -> tuple[date, datetime]:
    """Return a (date, aware datetime) pair `days` from now."""
    d = date.today() + timedelta(days=days)
    dt = datetime(d.year, d.month, d.day, hour, 0, tzinfo=_BERLIN_TZ)
    return d, dt


_GERMERING_DATE, _GERMERING_BEGIN = _future(14)
_NUERNBERG_DATE, _NUERNBERG_BEGIN = _future(21, hour=10)
_OBERURSEL_DATE, _OBERURSEL_BEGIN = _future(28, hour=10)


# ~20 km from Garching — always inside a 100 km radius.
GERMERING = Tournament(
    name="Herren basic in Germering",
    id = 10252,
    location="Germering",
    tournament_date=_GERMERING_DATE,
    begin_time=_GERMERING_BEGIN,
    latitude=48.134759,
    longitude=11.373936,
    level="basic",
    team_mode="Herren",
    registration_url="https://www.ebf.li/api/v1/tournaments/10252/",
)

# ~135 km from Garching — outside 100 km, inside 200 km.
NUERNBERG = Tournament(
    name="Mixed freestyle in Nürnberg - Schweinau",
    id=10092,
    location="Nürnberg",
    tournament_date=_NUERNBERG_DATE,
    begin_time=_NUERNBERG_BEGIN,
    latitude=49.423283,
    longitude=11.043864,
    level="freestyle",
    team_mode="Mixed",
    registration_url="https://www.ebf.li/api/v1/tournaments/10092/",
)

# ~300 km from Garching — outside any sensible radius.
OBERURSEL = Tournament(
    name="Mixed basic in Oberursel - TV Bommersheim",
    id=9527,
    location="Oberursel",
    tournament_date=_OBERURSEL_DATE,
    begin_time=_OBERURSEL_BEGIN,
    latitude=50.19879,
    longitude=8.60513,
    level="basic",
    team_mode="Mixed",
    registration_url="https://www.ebf.li/api/v1/tournaments/9527/",
)

# Deliberately NOT in distance order, so tests can prove sorting works.
ALL_TOURNAMENTS = [OBERURSEL, GERMERING, NUERNBERG]

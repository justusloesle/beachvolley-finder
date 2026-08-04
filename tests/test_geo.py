

import copy

from beach_finder.geo import filter_by_distance
from tests.fixtures import ALL_TOURNAMENTS, GERMERING, NUERNBERG


def _fresh() -> list:
    """Give each test its own copies.

    filter_by_distance writes `.distance` onto the objects it receives, so
    tests sharing the module-level fixtures would leak state into each
    other. Deep-copying keeps every test independent.
    """
    return copy.deepcopy(ALL_TOURNAMENTS)


def test_keeps_only_tournaments_within_radius():
    result = filter_by_distance(_fresh(), max_km=100)

    names = [t.name for t in result]
    assert names == [GERMERING.name]


def test_wider_radius_keeps_more():
    result = filter_by_distance(_fresh(), max_km=200)

    names = [t.name for t in result]
    assert GERMERING.name in names
    assert NUERNBERG.name in names
    assert len(result) == 2


def test_results_are_sorted_by_distance():
    result = filter_by_distance(_fresh(), max_km=500)

    distances = [t.distance for t in result]
    assert distances == sorted(distances)


def test_distance_is_populated_and_plausible():
    result = filter_by_distance(_fresh(), max_km=500)

    germering = next(t for t in result if t.name == GERMERING.name)
    # Garching -> Germering is roughly 25 km 
    assert 15 < germering.distance < 35


def test_zero_radius_returns_nothing():
    assert filter_by_distance(_fresh(), max_km=0) == []


def test_empty_input_returns_empty_list():
    assert filter_by_distance([], max_km=100) == []

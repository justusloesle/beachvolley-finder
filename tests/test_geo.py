"""Tests for the deterministic geo layer.

pytest is JUnit, lighter: functions prefixed `test_`, plain `assert`, no
class boilerplate. Run with `pytest` from the project root.
"""


# A trivial example so you can confirm pytest is wired up correctly:
def test_sanity():
    assert 1 + 1 == 2


# TODO: write the real test once filter_by_distance is implemented.
# Pattern:
#   1. build a couple of Tournament objects with known coordinates
#   2. call filter_by_distance(...) with a known origin + max_km
#   3. assert the near ones survive and the far ones are dropped
#
# def test_filter_by_distance_keeps_only_nearby():
#     ...

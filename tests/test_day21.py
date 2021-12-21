import io

import pytest

from days.day21 import first, second, parse_data, State, get_new_state

data = """Player 1 starting position: 4
Player 2 starting position: 8
"""


def test_parse_data():
    assert parse_data(io.StringIO(data)) == [4, 8]


def test_first():
    assert first(io.StringIO(data)) == 739785


def test_second():
    assert second(io.StringIO(data)) == 444356092776315


@pytest.mark.parametrize("state, dsum, expected", [
    (((3, 8), (5, 2), 0), 8, ((1, 9), (5, 2), 1)),
    (((3, 8), (5, 2), 1), 8, ((3, 8), (3, 5), 0)),
])
def test_get_new_state(state: State, dsum: int, expected: State):
    assert get_new_state(state, dsum) == expected

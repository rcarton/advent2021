import io

import pytest

from days.day17 import first, y, x, pos, Velocity, second

data = """target area: x=20..30, y=-10..-5
"""


def test_y():
    assert y(2, 7) == -7


def test_x():
    assert x(7, 7) == 28


@pytest.mark.parametrize("v, t", [
    ((7, 2), 7),
    ((6, 3), 9),
])
def test_pos(v: Velocity, t: int):
    # x=20..30, y=-10..-5
    px, py = pos(v, t)
    assert 20 <= px <= 30
    assert -10 <= py <= -5


def test_first():
    assert first(io.StringIO(data)) == 45


def test_second():
    assert second(io.StringIO(data)) == 112

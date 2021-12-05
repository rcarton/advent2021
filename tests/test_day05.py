import io

from days.day05 import first, second, OceanFloor

data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

expected = """.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111...."""


def test_from_string():
    assert str(OceanFloor.from_string(io.StringIO(data))) == expected


def test_first():
    assert first(io.StringIO(data)) == 5


def test_second():
    assert second(io.StringIO(data)) == 12

import io

from advent.days.day01 import first, nwise, second

input = io.StringIO("""199
200
208
210
200
207
240
269
260
263""")


def test_first():
    assert first(input) == 7


def test_nwise():
    assert list(nwise([1, 2, 3, 4, 5], 3)) == [
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 5),
    ]


def test_second():
    assert second(input) == 5

from io import StringIO

from days.day02 import first, second

data = StringIO("""forward 5
down 5
forward 8
up 3
down 8
forward 2""")


def test_first():
    assert first(data) == 150


def test_second():
    assert second(data) == 900

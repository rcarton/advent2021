import io

from days.day12 import first, second, parse_data

data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


def test_parse_data():
    assert parse_data(io.StringIO(data)) == {
        'A': ['start', 'c', 'b', 'end'],
        'b': ['start', 'A', 'd', 'end'],
        'c': ['A'],
        'd': ['b'],
        'end': ['A', 'b'],
        'start': ['A', 'b']
    }


def test_first():
    assert first(io.StringIO(data)) == 10


def test_second():
    assert second(io.StringIO(data)) == 36

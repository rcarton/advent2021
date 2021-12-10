import io

from days.day09 import first, second, parse_data

data = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def test_parse_data():
    entries = list(parse_data(io.StringIO(data)))
    displays, h = entries[0]
    assert len(displays) == 10
    assert h == [set('fdgacbe'), set('cefdb'), set('cefbgd'), set('gcbe')]


def test_first():
    assert first(io.StringIO(data)) == 15


def test_second():
    assert second(io.StringIO(data)) == 1134

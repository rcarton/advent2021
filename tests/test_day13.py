import io

from days.day13 import first, second, parse_data

data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def test_parse_data():
    dots, folds = parse_data(io.StringIO(data))
    assert len(dots) == 18
    assert folds == [
        (0, 7),
        (5, 0),
    ]


def test_first():
    assert first(io.StringIO(data)) == 17


def test_second():
    assert second(io.StringIO(data)) == -1

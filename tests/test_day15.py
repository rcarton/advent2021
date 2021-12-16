import io

from days.day15 import first, second, RepeatMatrix

data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


def test_first():
    assert first(io.StringIO(data)) == 40


def test_repeatmatrix():
    m = RepeatMatrix.from_string(data, int)
    assert m[0, 0] == 1
    assert m[0, 10] == 2
    assert m[10, 10] == 3
    assert m[49, 49] == 9

    assert m[3, 2] == 9
    assert m[3 + 10, 2] == 1
    assert m[3 + 20, 2] == 2
    assert m[3 + 20, 2 + 10] == 3


def test_second():
    assert second(io.StringIO(data)) == 315

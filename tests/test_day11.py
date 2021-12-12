import io

from advent.matrix import Matrix

from days.day11 import first, second, step

data = """11111
19991
19191
19991
11111"""


def test_step():
    g = Matrix.from_string(data, int)
    assert step(g) == 9
    assert str(g) == """34543
40004
50005
40004
34543"""


big_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def test_first():
    assert first(io.StringIO(big_data)) == 1656


def test_second():
    assert second(io.StringIO(big_data)) == 195

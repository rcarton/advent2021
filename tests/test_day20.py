import io

from days.day20 import first, second, parse_data

data = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


def test_parse_data():
    iea, sm = parse_data(io.StringIO(data))
    assert len(iea) == 512
    assert str(sm) == """#..#.
#....
##..#
..#..
..###
"""


def test_first():
    assert first(io.StringIO(data)) == 35


def test_second():
    assert second(io.StringIO(data)) == 3351

from collections import defaultdict
from dataclasses import dataclass
from typing import TextIO, Tuple, Dict, Iterator


@dataclass
class Line:
    start: Tuple[int, int]
    end: Tuple[int, int]


def points(line: Line) -> Iterator[Tuple[int, int]]:
    yield line.start
    x, y = line.start
    end_x, end_y = line.end
    while x != end_x or y != end_y:
        x = x - 1 if x > end_x else x + 1 if x < end_x else x
        y = y - 1 if y > end_y else y + 1 if y < end_y else y
        yield x, y


class OceanFloor:
    level: Dict[Tuple[int, int], int]
    support_diagonals: bool

    def __init__(self, support_diagonals: bool):
        self.level = defaultdict(lambda: 0)
        self.support_diagonals = support_diagonals

    def add_line(self, line: Line) -> None:
        is_diagonal = not (line.start[0] == line.end[0] or line.start[1] == line.end[1])
        if (not self.support_diagonals) and is_diagonal:
            # Discard lines that are not vertical or horizontal
            return

        for x, y in points(line):
            self.level[x, y] += 1

    def __repr__(self):
        xs, ys = zip(*self.level.keys())
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        s = ''
        for y in range(min_y, max_y + 1):
            s += ''.join('.' if self.level[x, y] < 1 else str(self.level[x, y]) for x in range(min_x, max_x + 1))
            if y < max_y:
                s += '\n'

        return s

    @classmethod
    def from_string(cls, data_s: TextIO, support_diagonals=False) -> 'OceanFloor':
        of = cls(support_diagonals)
        for line_s in data_s.readlines():
            start_s, end_s = line_s.split(' -> ')
            start = tuple(map(int, start_s.split(',')))
            end = tuple(map(int, end_s.split(',')))
            of.add_line(Line(start, end))

        return of


def first(data: TextIO) -> int:
    of = OceanFloor.from_string(data)
    return sum(1 for v in of.level.values() if v >= 2)


def second(data: TextIO) -> int:
    of = OceanFloor.from_string(data, support_diagonals=True)
    return sum(1 for v in of.level.values() if v >= 2)

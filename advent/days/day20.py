from collections import defaultdict
from typing import TextIO, Tuple, DefaultDict, List, Iterator

from advent.utils import binseq_to_int

Pos = Tuple[int, int]

ImageEnhancementAlgorithm = List[bool]


class SparseMatrix:
    data: DefaultDict[Pos, bool]
    is_negative: bool

    def __init__(self, s: str, is_negative: bool = False):
        self.is_negative = is_negative
        self.data = defaultdict(lambda: is_negative)

        for y, row in enumerate(s.splitlines()):
            for x, val in enumerate(row):
                self[x, y] = val == '#'

    def __getitem__(self, p: Pos) -> bool:
        return self.data[p]

    def __setitem__(self, p: Pos, value: bool) -> None:
        # Only store '.'s if negative matrix
        if value and self.is_negative:
            return
        # Only store '#'s if positive matrix
        if (not value) and (not self.is_negative):
            return

        assert not (not self.is_negative and value is False)

        self.data[p] = value

    def nb9(self, p: Pos) -> List[bool]:
        """These are in order for the 9 pixels"""
        return [self.data[p[0] + x, p[1] + y] for y in (-1, 0, 1) for x in (-1, 0, 1)]

    def all_pos(self) -> Iterator[Pos]:
        xs, ys = zip(*self.data.keys())
        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)

        # We need to make the largest square possible that can touch a pos/negative value
        for y in range(min_y - 2, max_y + 3):
            for x in range(min_x - 2, max_x + 3):
                yield x, y

    def px_to_index(self, p: Pos) -> int:
        return binseq_to_int(self.nb9(p))

    def __repr__(self):
        xs, ys = zip(*self.data.keys())
        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)

        s = ''
        for y in range(min_y, max_y + 1):
            s += ''.join('#' if self[x, y] else '.' for x in range(min_x, max_x + 1))
            s += '\n'
        return s


def step(iea: ImageEnhancementAlgorithm, sm: SparseMatrix) -> SparseMatrix:
    # If iea[0] is True, then we need to alternate matrices
    alternate = iea[0]

    new_sm = SparseMatrix('', not sm.is_negative if alternate else sm.is_negative)
    for p in sm.all_pos():
        new_sm[p] = iea[sm.px_to_index(p)]
    return new_sm


def parse_data(data: TextIO) -> Tuple[ImageEnhancementAlgorithm, SparseMatrix]:
    iea_s, image_s = data.read().strip().split('\n\n')
    iea = [c == '#' for c in iea_s.strip()]
    sm = SparseMatrix(image_s, is_negative=False)
    return iea, sm


def first(data: TextIO) -> int:
    iea, sm = parse_data(data)
    print(sm)
    sm = step(iea, sm)
    print("-----------------")
    print(sm)
    sm = step(iea, sm)
    print("-----------------")
    print(sm)

    # Can't count the lit pixels if it's negative because there are an infinite count
    assert sm.is_negative is False
    return len([v for v in sm.data.values() if v])


def second(data: TextIO) -> int:
    iea, sm = parse_data(data)
    for _ in range(50):
        sm = step(iea, sm)
    assert sm.is_negative is False
    return len([v for v in sm.data.values() if v])

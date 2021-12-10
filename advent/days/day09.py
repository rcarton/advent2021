from collections import deque
from functools import reduce

from advent.matrix import Matrix, Coord
from typing import TextIO, Set, List


def parse_data(data: TextIO) -> Matrix[int]:
    return Matrix.from_string(data.read(), int)


def first(data: TextIO) -> int:
    matrix = parse_data(data)
    return sum(matrix[c] + 1 for c in matrix.all_coords() if matrix[c] < min(matrix.neighbors(c)))


def second(data: TextIO) -> int:
    matrix = parse_data(data)
    explored: Set[Coord] = set()
    bassin_sizes: List[int] = []

    for c in matrix.all_coords():
        if c in explored:
            continue

        explored.add(c)

        # Skip, this is a ridge
        if matrix[c] == 9:
            continue

        bassin_size = 1

        # Explore the neighbors of c
        to_explore = deque(n for n in matrix.neighbor_coords(c))
        while to_explore:
            n = to_explore.pop()
            if n in explored:
                continue
            explored.add(n)

            if matrix[n] == 9:
                continue

            # It's part of the bassin
            bassin_size += 1
            # print(f'Adding m[{n}]={matrix[n]} to bassin, new size={bassin_size}')

            # Add the neighbors of the current coord
            to_explore.extend(nn for nn in matrix.neighbor_coords(n))

        bassin_sizes.append(bassin_size)

    return reduce(lambda prev, curr: prev * curr, sorted(bassin_sizes)[::-1][:3])

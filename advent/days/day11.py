from collections import deque
from typing import TextIO, Deque

from advent.matrix import Matrix, Coord


def step(grid: Matrix[int]) -> int:
    flash_count = 0

    # Increase energy level of all octopuses
    for c in grid.all_coords():
        assert grid[c] <= 9
        grid[c] += 1

    # Flashes
    for c in grid.all_coords():
        to_flash: Deque[Coord] = deque()

        if grid[c] > 9:
            to_flash.append(c)

        while to_flash:
            n = to_flash.pop()
            # Already flashed
            if grid[n] == 0:
                continue

            # Flashing
            flash_count += 1
            grid[n] = 0

            # Propagate
            for nn in grid.nbc8(n):
                if grid[nn] > 0:
                    grid[nn] += 1
                if grid[nn] > 9:
                    to_flash.append(nn)

    return flash_count


def first(data: TextIO) -> int:
    grid = Matrix.from_string(data.read(), int)
    return sum(step(grid) for _ in range(100))


def second(data: TextIO) -> int:
    grid = Matrix.from_string(data.read(), int)
    octopus_count = grid.width * grid.height

    step_count = 1
    while step(grid) != octopus_count:
        step_count += 1

        if step_count > 1_000_000:
            raise Exception('I gave up')

    return step_count

from typing import TextIO, List


def cost_to_move_crab(origin: int, dest: int) -> int:
    n = abs(dest - origin)
    if n == 0:
        return 0
    n += 1

    # Sum of an arithmetic series
    return int((n ** 2 - n) / 2)


def fuel_cost(position: int, crabs: List[int]) -> int:
    return sum(abs(position - i) for i in crabs)


def fuel_cost_v2(position: int, crabs: List[int]) -> int:
    return sum(cost_to_move_crab(i, position) for i in crabs)


def first(data: TextIO) -> int:
    crabs = [int(i) for i in data.read().strip().split(',')]
    return min(fuel_cost(i, crabs) for i in range(min(crabs), max(crabs) + 1))


def second(data: TextIO) -> int:
    crabs = [int(i) for i in data.read().strip().split(',')]
    return min(fuel_cost_v2(i, crabs) for i in range(min(crabs), max(crabs) + 1))

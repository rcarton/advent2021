import itertools as it
from collections import deque
from typing import TextIO, Tuple, TypeVar, Iterator, Iterable


def first(input: TextIO) -> int:
    nums = [int(num) for num in input.readlines()]
    return sum(1 if b > a else 0 for a, b in it.pairwise(nums))


def second(input: TextIO) -> int:
    nums = [int(num) for num in input.readlines()]
    sums = [sum(elements) for elements in nwise(nums, 3)]
    return sum(1 if b > a else 0 for a, b in it.pairwise(sums))


_T = TypeVar("_T")


def nwise(seq: Iterable[_T], count: int) -> Iterator[Tuple[_T, ...]]:
    last_elements = deque()
    for num in seq:
        last_elements.append(num)
        if len(last_elements) > count:
            last_elements.popleft()
        if len(last_elements) == count:
            yield tuple(last_elements)

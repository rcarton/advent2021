from collections import deque
from functools import reduce
from typing import TextIO, Optional, List, Iterable

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
MATCHING = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>',
}
OPENING = set(MATCHING.keys())
CLOSING = set(MATCHING.values())

COMPLETION_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def find_invalid_closing_character(line: str) -> Optional[str]:
    """Return the first invalid closing character found or None."""
    stack = deque()
    for c in line:
        if c in OPENING:
            stack.append(c)
        else:
            if c != MATCHING[stack.pop()]:
                return c


def finish_line(line: str) -> List[str]:
    """Return the first invalid closing character found or None."""
    stack = deque()
    for c in line:
        if c in OPENING:
            stack.append(c)
        else:
            stack.pop()
    result = []
    while stack:
        result.append(MATCHING[stack.pop()])

    return result


def score_completed_line(line: Iterable[str]) -> int:
    return reduce(lambda prev, curr: prev * 5 + COMPLETION_SCORES[curr], line, 0)


def first(data: TextIO) -> int:
    return sum(SCORES[invalid_char] for line in data.read().splitlines() if (
        invalid_char := find_invalid_closing_character(line)))


def second(data: TextIO) -> int:
    # Remove corrupted lines
    lines = [line for line in data.read().splitlines() if not find_invalid_closing_character(line)]
    scores = [score_completed_line(finish_line(line)) for line in lines]
    return sorted(scores)[int(len(scores)/2)]

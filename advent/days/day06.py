from typing import TextIO
from collections import Counter, deque

REPRO_RATE_FIRST_CYCLE = 9
REPRO_RATE = 7


def how_many_fishies(data: TextIO, max_days: int) -> int:
    counter = Counter(int(n) for n in data.read().strip().split(','))
    fishies = [counter[i] for i in range(REPRO_RATE)]
    first_cycle_fishies = deque(counter[n] for n in range(REPRO_RATE, REPRO_RATE_FIRST_CYCLE))

    for day in range(max_days):
        day_mod = day % REPRO_RATE
        first_cycle_fishies.append(fishies[day_mod])
        fishies[day_mod] += first_cycle_fishies.popleft()

    return sum(fishies) + sum(first_cycle_fishies)


def first(data: TextIO) -> int:
    return how_many_fishies(data, 80)


def second(data: TextIO) -> int:
    return how_many_fishies(data, 256)

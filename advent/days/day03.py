from typing import TextIO, List, Callable

from advent.utils import binseq_to_int


def first(data: TextIO) -> int:
    data = data.read().splitlines()

    # Find the most common bit for each position by counting the number of 1s, if there are 6 entries, then
    # 1 is the most common if there are 4 or more 1s, otherwise 0 is the most common. This does not support
    # cases where there's an equal number of 0s and 1s, we assume this does not happen in the input.
    most_common_bit_per_position = [int(sum(map(int, i)) > len(i) / 2) for i in zip(*data)]

    # Turn 0s into 1s and vice versa
    least_common_bit_per_position = [int(not i) for i in most_common_bit_per_position]

    return binseq_to_int(most_common_bit_per_position) * binseq_to_int(least_common_bit_per_position)


def oxygen_generator_rating(data: List[List[int]]) -> int:
    def most_common_bit_for_position(candidates: List[List[int]], i: int) -> int:
        return int(sum(map(lambda bits: bits[i], candidates)) >= len(candidates) / 2)

    return compute_rating(data, most_common_bit_for_position)


def co2_scrubber_rating(data: List[List[int]]) -> int:
    def least_common_bit_for_position(candidates: List[List[int]], i: int) -> int:
        return int(not sum(map(lambda bits: bits[i], candidates)) >= len(candidates) / 2)

    return compute_rating(data, least_common_bit_for_position)


def compute_rating(data: List[List[int]], bit_criteria_fn: Callable[[List[List[int]], int], int]) -> int:
    """
    Compute a rating by filtering every data entry using bit_criteria_fn until only one entry is left.
    """
    candidates = list(data)

    for i in range(len(data[0])):
        bit_criteria = bit_criteria_fn(candidates, i)
        candidates = list(filter(lambda bits: bits[i] == bit_criteria, candidates))
        if len(candidates) == 1:
            return binseq_to_int(candidates[0])

    raise Exception('Generator rating not found')


def second(data: TextIO) -> int:
    data = [list(map(int, i)) for i in data.read().splitlines()]
    return oxygen_generator_rating(data) * co2_scrubber_rating(data)

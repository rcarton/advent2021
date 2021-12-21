from typing import Sequence, Union, Optional


def binseq_to_int(binseq: Sequence[Union[str, int, bool]]) -> int:
    """Turn a sequence that can be mapped to bits into its integer representation:

    Examples:
        - '101' -> 5
        - [True, False, True] -> 5
        - [1, 0, 1] -> 5

    """
    return sum(int(j) << i for i, j in enumerate(reversed(binseq)))


def add_wrap(val: int, incr: int, max_val: int, start_at_one: Optional[bool] = True):
    """Add incr to val, and wrap around at 1 if val+incr > max_val"""
    return (val + incr - 1) % max_val + (1 if start_at_one else 0)

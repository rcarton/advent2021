from typing import Sequence, Union


def binseq_to_int(binseq: Sequence[Union[str, int, bool]]) -> int:
    """Turn a sequence that can be mapped to bits into its integer representation:

    Examples:
        - '101' -> 5
        - [True, False, True] -> 5
        - [1, 0, 1] -> 5

    """
    return sum(int(j) << i for i, j in enumerate(reversed(binseq)))

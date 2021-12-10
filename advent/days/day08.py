import itertools as it
from collections import Counter, defaultdict
from typing import TextIO, Dict, Set, Tuple, List, Iterator

DIGITS: Dict[int, Set[str]] = {
    0: set('abcefg'),
    1: set('cf'),
    2: set('acdeg'),
    3: set('acdfg'),
    4: set('bcdf'),
    5: set('abdfg'),
    6: set('abdefg'),
    7: set('acf'),
    8: set('abcdefg'),
    9: set('abcdfg'),
}
SEGMENTS_TO_DIGITS = {''.join(sorted(segments)): num for num, segments in DIGITS.items()}
SEGMENT_EXPECTED_COUNTS = Counter(it.chain(*map(list, DIGITS.values())))

# 4 -> {'e',} If a segment is found 4 times in the display of the digits, then it has to be the 'e' segment
COUNT_BY_SEGMENT: Dict[int, Set[str]] = defaultdict(set)
for segment, count in SEGMENT_EXPECTED_COUNTS.items():
    COUNT_BY_SEGMENT[count].add(segment)

# Segment candidates for the mapping, for example 'a' -> {'b', 'c'} means 'a' in the input could either be 'b' or 'c'
Candidates = Dict[str, set[str]]

# Solved segments, 'b' -> 'c' means 'b' in the input is actually 'c'
Solved = Dict[str, str]

Display = Set[str]
Output = List[Display]
Entry = Tuple[List[Display], Output]


class SegmentPuzzle:
    """
    This class represents a Segment Puzzle. The goal is to find the mapping from the scrambled segments in the initial
    display and find a valid mapping for each puzzle segment to the actual segment.

    For instance, if in the scrambled puzzle the 'e' segment is normally represented as 'a' (top segment), then the
    solution should contain: 'e': 'a'.
    """
    candidates: Candidates
    solved: Solved
    digits: List[Display]
    output: Output

    def __init__(self, digits: List[Display], output: Output):
        # Initially every letter can map to any other letter
        self.candidates = {segment: set('abcdefg') for segment in 'abcdefg'}
        self.solved = {}
        self.digits = digits
        self.output = output

    def segment_count_in_all_digits(self) -> None:
        """
        Since the digits contain every digit once, we know that in a given segment is featured exactly n times. We can
        use this to narrow down the selection, for example the 'e' segment is only shown once, and is the only segment
        shown exactly 4 times over all the digits, which means any segment present exactly 4 times has to be e.

        This first heuristic will identify 3 segments, and narrow down the other ones to 2 options each.
        We could probably stop here and brute force all the other possibilities (2*2*2*2). Or apply another heuristic.
        """
        segment_counts = Counter(it.chain(*self.digits))
        for segment, count in segment_counts.items():
            self.candidates[segment] &= COUNT_BY_SEGMENT[count]

    def solve(self) -> Solved:
        # First heuristic, use expected counts of segments to identify f, b, and e, and restrict the other to 2 options
        self.segment_count_in_all_digits()

        # Second heuristic, could use the count of segments per digit
        # Not necessary because at this point there are a total of 16 possible candidates, which we can brute force
        # through quickly

        # At this point we have narrowed down self.candidates: most segments have 1 or 2 possible translations
        possible_solutions: List[Solved] = self.get_possible_solutions(self.candidates, {})
        for solution in possible_solutions:
            if self.is_solution_valid(self.digits, solution):
                return solution

        raise Exception('No valid solution found')

    @staticmethod
    def get_possible_solutions(candidates: Candidates, solved: Solved) -> List[Solved]:
        """
        This is the most complicated part of this - generate all the possible solutions knowing what we have already
        ruled out using heuristics. By using more heuristics we can reduce the amount of possible solutions, which
        means we wouldn't have to test as many to find the valid one.
        """
        if not candidates:
            return [solved]

        candidates = candidates.copy()
        next_key = next(iter(candidates.keys()))
        possibles = candidates.pop(next_key)
        results = []
        for possible in possibles:
            new_solved = solved.copy()
            new_solved[next_key] = possible
            results += SegmentPuzzle.get_possible_solutions(candidates, new_solved)

        return results

    @staticmethod
    def is_solution_valid(digits: List[Display], solution: Solved) -> bool:
        """Try translating every digit and looking it up in the scrambled digits."""
        all_correct_digits = list(DIGITS.values())
        for d in digits:
            translated = set(''.join(solution[letter] for letter in d))
            if translated not in all_correct_digits:
                return False
        return True

    def is_solved(self) -> bool:
        return all(len(n) == 1 for n in self.candidates.values())


def translate_display(display: Display, mapping: Solved) -> int:
    return SEGMENTS_TO_DIGITS[''.join(sorted(''.join(mapping[letter] for letter in display)))]


def translate_output(output: Output, mapping: Solved) -> int:
    return int(''.join([str(translate_display(d, mapping)) for d in output]))


def parse_data(data: TextIO) -> Iterator[Entry]:
    for line in data:
        left, right = line.strip().split(' | ')
        yield [set(segment) for segment in left.split(' ')], [set(segment) for segment in right.split(' ')]


def first(data: TextIO) -> int:
    entries = parse_data(data)

    # Count 1s, 4s, 7s, and 8s by looking at the length of the digit being display (== number of segments on)
    all_outputs = it.chain(*[o for _, o in entries])
    unique_counts = {len(segments) for segments in (DIGITS[1], DIGITS[4], DIGITS[7], DIGITS[8])}

    return sum(1 if len(o) in unique_counts else 0 for o in all_outputs)


def second(data: TextIO) -> int:
    entries = parse_data(data)
    total = 0
    for digits, output in entries:
        # Mapping is the segment mapping to go from the scrambled input to a normal input
        mapping = SegmentPuzzle(digits, output).solve()

        # We use the mapping to translate the segments into their normal segments, then the output into a number
        total += translate_output(output, mapping)

    return total

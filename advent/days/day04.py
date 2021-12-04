import itertools as it
import re
from typing import TextIO, Set, List, Tuple


class Bingo(Exception):
    """This is bad practice but for fun, the code looks more like a game of Bingo if you raise when you get one."""
    pass


class Board:
    """
    Mutable board, keep track of all the nums in a set to know if we even need to go through the rows and columns.
    Rows and columns are sets because the order does not matter.
    """
    all_nums: Set[int]
    rows: List[Set[int]]
    columns: List[Set[int]]

    def __init__(self, board: List[List[int]]):
        self.all_nums = set(it.chain(*board))
        self.rows = [set(r) for r in board]
        self.columns = [set(c) for c in zip(*board)]

    def draw_number(self, num: int) -> None:
        if num not in self.all_nums:
            return

        self.all_nums.discard(num)

        for row_or_col in it.chain(self.rows, self.columns):
            row_or_col.discard(num)
            if len(row_or_col) == 0:
                # OH MY GOD BINGO, HONEY I GOT A BINGO!
                raise Bingo

    def compute_score(self, last_num: int):
        return last_num * sum(self.all_nums)

    @staticmethod
    def from_board_string(bs: str) -> 'Board':
        nums = [[int(n) for n in re.split(r"\s+", row.strip())] for row in bs.splitlines()]
        return Board(nums)


def parse_data(data: TextIO) -> Tuple[List[int], List[Board]]:
    big_string = data.read()
    drawn_string, *board_strings = big_string.split('\n\n')
    drawn = [int(n) for n in drawn_string.split(',')]
    boards = [Board.from_board_string(b) for b in board_strings]
    return drawn, boards


def first(data: TextIO) -> int:
    drawn, boards = parse_data(data)

    for num in drawn:
        for board in boards:
            try:
                board.draw_number(num)
            except Bingo:
                return board.compute_score(num)

    raise Exception('No bingo :(')


def second(data: TextIO) -> int:
    drawn, boards = parse_data(data)
    boards_that_did_not_bingo = set(boards)

    for num in drawn:
        for board in list(boards_that_did_not_bingo):
            try:
                board.draw_number(num)
            except Bingo:
                boards_that_did_not_bingo.discard(board)

                if len(boards_that_did_not_bingo) == 0:
                    return board.compute_score(num)

    raise Exception('No bingo :(')

from functools import reduce
from typing import Union, Optional, List, TextIO, Literal, Tuple
import math
import itertools as it


def is_number(v):
    return type(v) == int


def split_num(n: int) -> Tuple[int, int]:
    return n // 2, math.ceil(n / 2)


class Pair:
    left: Union['Pair', int]
    right: Union['Pair', int]

    parent: 'Pair'

    def __init__(self, left: Union['Pair', int], right: Union['Pair', int], parent: Optional['Pair'] = None):
        self.parent = parent
        self.left = left
        self.right = right

    def __add__(self, b) -> 'Pair':
        # This probably shouldn't mutate self and b but eh.
        # p = Pair(self, b)
        # self.parent = p
        # b.parent = p

        # I DEFINITELY shouldn't have mutated. Keeping this for posterity.
        a = Pair.from_string(str(self))
        b = Pair.from_string(str(b))
        p = Pair(a, b)
        a.parent = p
        b.parent = p

        # Keep reducing
        while p.reduce_once():
            pass

        return p

    def reduce_once(self) -> bool:
        return self.explode() or self.split()

    def explode_up(self, number: int, side: Literal["left", "right"]) -> None:
        def get_side(p: Pair) -> Union[Pair, int]:
            return p.left if side == "left" else p.right

        def get_other_side(p: Pair) -> Union[Pair, int]:
            return p.left if side == "right" else p.right

        prev = self
        curr = self.parent
        # Go up until we find a parent for which the current node is the right child if exploding left
        while curr is not None and prev == get_side(curr):
            prev, curr = curr, curr.parent

        if curr is None:
            return

        # It's a number, easy, we bump and return
        if is_number(get_side(curr)):
            if side == "left":
                curr.left += number
            else:
                curr.right += number
            return

        # It's a pair, we have to go down and find the right most pair if exploding left, leftmost pair if exploring
        # right
        curr = get_side(curr)
        while not is_number(get_other_side(curr)):
            curr = get_other_side(curr)

        if side == "left":
            curr.right += number
        else:
            curr.left += number

    def explode(self, depth: int = 0) -> bool:
        if depth == 4:
            self.explode_up(self.left, "left")
            self.explode_up(self.right, "right")

            if self.parent.right == self:
                self.parent.right = 0
            else:
                self.parent.left = 0
            return True

        if not is_number(self.left):
            r = self.left.explode(depth + 1)
            if r:
                return True
        if not is_number(self.right):
            return self.right.explode(depth + 1)

        return False

    def split(self) -> bool:
        if type(self.left) == Pair:
            if self.left.split():
                return True
        else:
            if self.left >= 10:
                self.left = Pair(*split_num(self.left), self)
                return True

        if type(self.right) == Pair:
            if self.right.split():
                return True
        else:
            if self.right >= 10:
                self.right = Pair(*split_num(self.right), self)
                return True
        return False

    def magnitude(self):
        mag_left = 3 * (self.left if is_number(self.left) else self.left.magnitude())
        mag_right = 2 * (self.right if is_number(self.right) else self.right.magnitude())
        return mag_left + mag_right

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    @classmethod
    def from_array(cls, arr: List) -> 'Pair':
        left, right = arr
        pair = cls(
            left if type(left) == int else cls.from_array(left),
            right if type(right) == int else cls.from_array(right),
        )
        if type(left) != int:
            pair.left.parent = pair
        if type(right) != int:
            pair.right.parent = pair

        return pair

    @classmethod
    def from_string(cls, s: str) -> 'Pair':
        # Nothing to see here.
        return cls.from_array(eval(s))


def first(data: TextIO) -> int:
    pairs = [Pair.from_string(line) for line in data.readlines()]
    return reduce(lambda prev, curr: prev + curr, pairs).magnitude()


def second(data: TextIO) -> int:
    pairs = [Pair.from_string(line) for line in data.readlines()]
    return max((p1 + p2).magnitude() for p1, p2 in it.permutations(pairs, 2))

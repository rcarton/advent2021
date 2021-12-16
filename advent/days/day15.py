from collections import deque
from typing import TextIO, Set, Tuple, List, TypeVar

from advent.matrix import Matrix, Coord

Visited = Set[Coord]
Element = Tuple[int, Visited, Coord]

T = TypeVar('T')


class RepeatMatrix(Matrix):
    base_width: int
    base_height: int

    def __init__(self, data: List[T], width: int, height: int):
        super().__init__(data, width, height)
        self.base_width = width
        self.base_height = height

        self.width = width * 5
        self.height = height * 5

    def __in_base_matrix(self, coord: Coord):
        row, col = coord
        return row < self.base_height and col < self.base_width

    def __get_index(self, coord: Coord):
        row, col = coord
        if not (self.is_valid_coord(coord) and self.__in_base_matrix(coord)):
            raise IndexError(f'Coord out of range {coord}')
        return row * self.base_width + col

    def __getitem__(self, coord: Coord) -> T:
        if self.__in_base_matrix(coord):
            return self.data[self.__get_index(coord)]

        # Find the base cell
        row, col = coord
        base_row = row % self.base_height
        base_column = col % self.base_width
        base_value = self.data[self.__get_index((base_row, base_column))]

        # Find the offset based on which matrix copy it is
        vert_offset = row // self.base_height
        horiz_offset = col // self.base_width
        assert vert_offset < 5 and horiz_offset < 5
        total_offset = vert_offset + horiz_offset

        # Reset to 1
        new_value = base_value + total_offset
        if new_value > 9:
            new_value -= 9
        assert 0 < new_value < 10
        return new_value


def traverse(m: Matrix[int]) -> int:
    min_risk = {
        (0, 0): 0,
    }
    to_visit = deque([(0, 0)])
    to_visit_set = set(to_visit)

    while to_visit:
        # Could improve by always visiting the lowest score first
        c = to_visit.popleft()
        to_visit_set.remove(c)

        current_risk = min_risk[c]

        for n in m.neighbor_coords(c):
            if (n in min_risk and current_risk + m[n] < min_risk[n]) or n not in min_risk:
                # Update the min risk for this neighbor
                min_risk[n] = current_risk + m[n]

                if n not in to_visit_set:
                    to_visit_set.add(n)
                    to_visit.append(n)

    return min_risk[m.height - 1, m.width - 1]


def first(data: TextIO) -> int:
    m = Matrix.from_string(data.read(), int)
    return traverse(m)


def second(data: TextIO) -> int:
    m = RepeatMatrix.from_string(data.read(), int)
    return traverse(m)

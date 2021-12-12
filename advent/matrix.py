from typing import List, TypeVar, Generic, Tuple, Callable, Optional, Iterator
import itertools as it

T = TypeVar('T')

# row, col
Coord = Tuple[int, int]


class Matrix(Generic[T]):
    data: List[T]
    width: int
    height: int

    def __init__(self, data: List[T], width: int, height: int):
        self.data = list(data)
        assert len(self.data) == width * height
        self.width = width
        self.height = height

    def is_valid_coord(self, coord: Coord):
        return 0 <= coord[0] < self.height and 0 <= coord[1] < self.width

    def __get_index(self, coord: Coord):
        row, col = coord
        if not self.is_valid_coord(coord):
            raise IndexError(f'Coord out of range {coord}')
        return row * self.width + col

    def __getitem__(self, coord: Coord) -> T:
        return self.data[self.__get_index(coord)]

    def __setitem__(self, coord: Coord, value: T) -> None:
        self.data[self.__get_index(coord)] = value

    @classmethod
    def from_string(cls, data: str, fn: Optional[Callable[[str], T]] = None) -> 'Matrix[T]':
        rows = data.splitlines()
        height = len(rows)
        width = len(rows[0])
        data_as_array = [fn(v) if fn else v for v in it.chain(*rows)]
        return cls(data_as_array, width, height)

    def all_coords(self) -> Iterator[Coord]:
        for x in range(self.height):
            for y in range(self.width):
                yield x, y

    def neighbor_coords(self, coord: Coord, include_diagonals: bool = False) -> List[Coord]:
        row, col = coord
        coords = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        if include_diagonals:
            coords += [(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]

        return [c for c in coords if self.is_valid_coord(c)]

    def neighbors(self, coord: Coord, include_diagonals: bool = False) -> List[T]:
        return [self[c] for c in self.neighbor_coords(coord, include_diagonals) if self.is_valid_coord(c)]

    def nb8(self, coord: Coord) -> List[T]:
        return self.neighbors(coord, include_diagonals=True)

    def nbc8(self, coord: Coord) -> List[Coord]:
        return self.neighbor_coords(coord, include_diagonals=True)

    def __str__(self):
        out = ''
        for row in range(self.height):
            for col in range(self.width):
                out += str(self[row, col])
            out += '\n'
        return out[:-1]

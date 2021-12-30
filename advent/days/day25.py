from typing import List, Tuple, TextIO


class RotatoMatrixo:
    data: List[List[str]]
    width: int
    height: int

    def __init__(self, data: List[List[str]], width: int, height: int):
        self.data = data
        self.width = width
        self.height = height

    def __getitem__(self, rowcol: Tuple[int, int]) -> str:
        return self.data[rowcol[0]][rowcol[1]]

    def step(self) -> int:
        count = 0
        for direction in ('>', 'v'):
            new_data = [self.data[row][:] for row in range(self.height)]
            for row in range(self.height):
                for column in range(self.width):
                    c = self[row, column]
                    if c != direction:
                        continue
                    nr, nc = (row, (column + 1) % self.width) if c == '>' else ((row + 1) % self.height, column)
                    if self.data[nr][nc] == '.':
                        count += 1
                        new_data[row][column] = '.'
                        new_data[nr][nc] = c
            self.data = new_data

        return count

    def __repr__(self):
        s = '\n'
        for r in range(self.height):
            s += ''.join(self.data[r]) + '\n'
        return s

    @classmethod
    def from_string(cls, s: str) -> 'RotatoMatrixo':
        data = [[c for c in line] for line in s.split('\n') if line]
        w = len(data[0])
        h = len(data)

        return RotatoMatrixo(data, w, h)


def first(data: TextIO) -> int:
    rm = RotatoMatrixo.from_string(data.read().strip())

    change = -1
    count = 0
    while change != 0:
        change = rm.step()
        count += 1

    return count


def second(data: TextIO) -> int:
    return -1

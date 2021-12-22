import itertools as it
import re
from collections import defaultdict
from functools import reduce
from typing import Tuple, TextIO, List, cast, Optional

# (start, end), inclusive of start and end
Coord = Tuple[int, int]
Cube = Tuple[Coord, Coord, Coord]
CubeFlip = Tuple[bool, Cube]

# A universe is a list of cubes that are on, with no intersection
# between each other
Universe = List[Cube]


def intersect(c1: Cube, c2: Cube) -> Optional[Cube]:
    """This is a 3D intersect (actually n dims)."""
    c = tuple((max(c1[dim][0], c2[dim][0]), min(c1[dim][1], c2[dim][1])) for dim in range(len(c1)))

    # Check for impossible cubes
    if any(dim[0] > dim[1] for dim in c):
        return None

    return c


def size(c: Cube) -> int:
    return reduce(lambda prev, curr: prev * curr, [abs(end - start) + 1 if end >= start else 0 for start, end in c], 1)


def in_cube(c1: Cube, c2: Cube) -> bool:
    """Return True if c1 is contained by c2."""
    for dim in range(len(c1)):
        if c1[dim][0] < c2[dim][0] or c1[dim][1] > c2[dim][1]:
            return False
    return True


def remove_cube(c1: Cube, c2: Cube) -> Universe:
    """
    Remove c2 from c1.
    This returns a list of cubes that do not intersect.

    If c1 is contained by c2, then no cube is returned.

    c1 - c2 is a list of cubes because if they intersect it can only be represented
    by multiple cubes.
    """
    if intersect(c1, c2) is None:
        return [c1]
    if in_cube(c1, c2):
        return []

    c2 = intersect(c1, c2)

    # For a cube, there are at most 27 possible cubes
    # In 1D (aka we're removing a range from another), it's at most 3
    # it's 3**number_of_dims:
    all_ranges = [[(c1[dim][0], c2[dim][0] - 1), (c2[dim][0], c2[dim][1]), (c2[dim][1] + 1, c1[dim][1])] for dim in
                  range(len(c1))]
    all_ranges = [[(start, end) for start, end in ranges if start <= end] for ranges in all_ranges]
    all_cubes = it.product(*all_ranges)

    # Now remove the one intersection cube
    all_cubes = filter(lambda c: c != c2, all_cubes)

    # We could merge some cubes that share dimensions
    return all_cubes


def remove(u: Universe, c: Cube) -> Universe:
    new_u = []
    # Cubes that need to be removed
    for cube in u:
        new_u.extend(remove_cube(cube, c))

    return new_u


def add(u: Universe, c: Cube) -> Universe:
    new_u = [c]
    # Cubes that need to be removed

    for cube in u:
        # We're adding cube - c to the universe
        # if there's no intersection, this adds the whole cube
        # if cube is contained by c, then this adds nothing
        # if there is an intersection, it'll add multiple cubes
        new_u.extend(remove_cube(cube, c))

    return new_u

FIFTY_CUBE = ((-50, 50),) * 3


def count_universe(u: Universe) -> int:
    return sum(size(c) for c in u)

def parse_data(data: TextIO) -> List[Tuple[bool, Cube]]:
    r = []
    for line in data.read().strip().splitlines():
        on_off_s, coords_s = line.split(' ')
        on_off = on_off_s == 'on'
        coords = list(map(int, re.findall(r'[-\d]+', coords_s)))
        r.append((on_off, (coords[:2], coords[2:4], coords[4:6])))

    return cast(List[Tuple[bool, Cube]], r)

def first(data: TextIO) -> int:
    cube_flips = parse_data(data)

    # We only care about stuff in our fifty cube
    cube_flips = [(on_off, intersect(cube, FIFTY_CUBE)) for on_off, cube in cube_flips]
    cube_flips = [(on_off, cube) for on_off, cube in cube_flips if cube is not None]

    # Dumb universe for now using a map
    u = defaultdict(lambda: False)
    for on_off, cube in cube_flips:
        for x, y, z in it.product(*[range(start, end + 1) for start, end in cube]):
            u[x, y, z] = on_off

    return sum(u.values())


def second(data: TextIO) -> int:
    cube_flips = parse_data(data)

    u = []
    for on_off, c in cube_flips:
        if on_off:
            u = add(u, c)
        else:
            u = remove(u, c)

    return count_universe(u)

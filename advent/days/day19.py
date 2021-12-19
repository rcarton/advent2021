import itertools as it
import re
from typing import Tuple, Optional, List, TextIO, Literal

Pos = Tuple[int, int, int]
Beacon = Pos

# An orientation is a number of rotation by 90deg: 0, 1, 2, 3 for each axis
Orientation = Tuple[int, int, int]


def rotate_around_axis(p: Pos, axis: Literal[0, 1, 2]) -> Pos:
    """Rotate by 90 degrees once against an axis, x=0, y=1, z=2"""
    pp = [0, 0, 0]
    pp[axis] = p[axis]
    pp[(axis + 1) % 3] = p[(axis + 2) % 3]
    pp[(axis + 2) % 3] = -p[(axis + 1) % 3]

    return tuple(pp)


def rotate_to_orientation(p: Pos, o: Orientation) -> Pos:
    """
    Apply a succession of rotations along the x, y, and z axis.

    (1, 2, 3) means rotate the point:
        - once around the x axis (counter clockwise)
        - twice around the y axis
        - thrice around the z axis
    """
    if o == (0, 0, 0):
        # Nothing to do
        return p

    for axis, count in enumerate(o):
        for _ in range(count):
            p = rotate_around_axis(p, axis)
    return p


def all_orientations() -> List[Orientation]:
    # This has orientations that are equivalent because they produce the same point
    all_rot = list(it.product(*[list(range(4)) for _ in range(3)]))
    p = (5, 3, 7)

    found = set()
    unique_rots = []
    for rot in all_rot:
        pp = rotate_to_orientation(p, rot)
        if pp not in found:
            found.add(pp)
            unique_rots.append(rot)

    assert len(unique_rots) == 24
    return unique_rots


ALL_ORIENTATIONS = all_orientations()


class Scanner:
    id: int
    pos: Optional[Pos]
    beacons: List[Beacon]

    def __init__(self, s: str):
        id_line, *beacon_lines = s.strip().split('\n')
        self.id = int(re.findall(r'\d+', id_line)[0])
        self.beacons = [eval(line) for line in beacon_lines]

        if self.id == 0:
            self.pos = (0, 0, 0)
        else:
            self.pos = None

    def __repr__(self):
        return f'Scanner id={self.id} pos={"unknown" if self.pos is None else self.pos}'


def translate(bs: List[Beacon], new_origin: Pos) -> List[Beacon]:
    """Make all the beacons in the list be relative to new_origin"""
    return [(x - new_origin[0], y - new_origin[1], z - new_origin[2]) for x, y, z in bs]


def rotate(bs: List[Beacon], orientation: Orientation) -> List[Beacon]:
    """Rotate the list of beacons according to an orientation"""
    return [rotate_to_orientation(b, orientation) for b in bs]


Overlap = Tuple[int, int, Orientation]


def overlap(s1: Scanner, s2: Scanner) -> Optional[Overlap]:
    """
    Return True if 12 or more beacons overlap between scanners.

    The scanners overlap if we can find an orientation and an origin that has 12 or more beacons at the same position.
    To find a valid origin, we take a beacon in s1, use it as an origin and adjust the pos of all the other beacons in
    s1 so that this beacon is at (0,0,0). Then for every beacon in s2, we do the same and see if the resulting lists
    of beacons have 12 or more beacons in common, then we keep doing it for every possible orientation.
    """
    # s1's position must have been found
    assert s1.pos is not None
    assert s2.pos is None

    # Take a beacon
    for b1_index, b1 in enumerate(s1.beacons):
        # Set b1 as the reference
        b1s = set(translate(s1.beacons, b1))

        # Rotations are more expensive, do them first (so we're rotating 24 times, and then translating for every beacon
        for orientation in ALL_ORIENTATIONS:
            rotated_b2s = rotate(s2.beacons, orientation)
            for b2_index, b2 in enumerate(rotated_b2s):
                # Set b2 as the reference
                b2s = set(translate(rotated_b2s, b2))

                common = b1s & b2s
                if len(common) >= 12:
                    # print(f'Found match at b1={b1} == b2={s2.beacons[b2_index]} and orientation={orientation}')
                    return b1_index, b2_index, orientation

    return None


def calibrate_scanner(known_scanner: Scanner, scanner: Scanner, overlapped: Overlap) -> None:
    """Calibrate a scanner given a "good" scanner and an unknown one that overlaps."""
    known_b_index, invalid_b_index, orientation = overlapped

    # Reorient all beacons according to the orientation we found a match with
    scanner.beacons = rotate(scanner.beacons, orientation)

    # Now the unknown beacon is oriented but still shifted

    # Translate: if valid beacon is at 3, 6 and invalid is at 7, 9
    # Then all beacons must be shifted -4, -3 to be at the right position
    valid_beacon = known_scanner.beacons[known_b_index]
    invalid_beacon = scanner.beacons[invalid_b_index]
    shift_x, shift_y, shift_z = [valid_beacon[i] - invalid_beacon[i] for i in range(3)]
    scanner.beacons = [(x + shift_x, y + shift_y, z + shift_z) for x, y, z in scanner.beacons]

    # Adjust the position of the unknown beacon
    scanner.pos = shift_x, shift_y, shift_z


def resolve(scanners: List[Scanner]) -> None:
    """Calibrate all the scanners by finding overlaps between resolved scanners and unresolved ones."""
    to_resolve = scanners[1:]
    resolved = {scanners[0]}

    while resolved:
        s1 = resolved.pop()

        # Find all the matches for s1
        for s2 in to_resolve[:]:
            overlapped = overlap(s1, s2)
            if overlapped:
                # Fix s2
                calibrate_scanner(s1, s2, overlapped)

                to_resolve.remove(s2)
                resolved.add(s2)


def parse_data(data: TextIO) -> List[Scanner]:
    return [Scanner(s) for s in data.read().split('\n\n')]


def manhattan(p1: Pos, p2: Pos) -> int:
    return sum(abs(a - b) for a, b in zip(p1, p2))


def first(data: TextIO) -> int:
    scanners = parse_data(data)
    resolve(scanners)

    beacons = set()
    for s in scanners:
        beacons |= set(s.beacons)
    return len(beacons)


def second(data: TextIO) -> int:
    scanners = parse_data(data)
    resolve(scanners)
    return max(manhattan(s1.pos, s2.pos) for s1, s2 in it.combinations(scanners, 2))
